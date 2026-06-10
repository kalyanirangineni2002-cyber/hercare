from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from .models import HealthReport
from .forms import HealthReportForm
from google import genai
from google.genai import types
import json

@login_required
def reports_home(request):
    """View and search user's uploaded health reports."""
    query = request.GET.get('q', '')
    report_type = request.GET.get('type', '')
    
    reports = HealthReport.objects.filter(user=request.user)
    
    if query:
        reports = reports.filter(
            Q(title__icontains=query) |
            Q(doctor_name__icontains=query) |
            Q(hospital_clinic__icontains=query) |
            Q(notes__icontains=query)
        )
        
    if report_type:
        reports = reports.filter(report_type=report_type)
        
    context = {
        'reports': reports,
        'query': query,
        'report_type': report_type,
        'types': HealthReport.REPORT_TYPE_CHOICES,
    }
    return render(request, 'health_reports/reports.html', context)

@login_required
def upload_report(request):
    """Upload a new health report."""
    if request.method == 'POST':
        form = HealthReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            
            # Read file bytes and run Gemini analysis
            api_key = getattr(settings, 'GEMINI_API_KEY', None)
            if api_key:
                try:
                    file_path = report.file.path
                    mime_type = request.FILES['file'].content_type
                    
                    # Read the uploaded file bytes
                    with open(file_path, 'rb') as f:
                        file_bytes = f.read()
                    
                    client = genai.Client(api_key=api_key)
                    
                    # Map language code to human-readable name for prompt
                    lang_map = {
                        'en': 'English',
                        'te': 'Telugu',
                        'hi': 'Hindi',
                        'ta': 'Tamil'
                    }
                    target_lang = lang_map.get(report.summary_language, 'English')
                    
                    prompt = f"""
                    You are a professional medical AI assistant specialized in translating and explaining health reports in simple terms.
                    Analyze the attached medical document (PDF or image).
                    
                    Provide the following:
                    1. A clear, empathetic explanation of the report in simple, layperson-friendly language. This explanation must be written entirely in the requested language: {target_lang}.
                    2. A list of key values and any abnormal findings. Highlight what is out of range or warrants attention. Explain why it matters in simple terms. This section must also be written entirely in the requested language: {target_lang}.
                    
                    Return the output STRICTLY as a JSON object with the following format:
                    {{
                        "explanation": "Your explanation in {target_lang} here...",
                        "abnormal_findings": "Your bulleted list of abnormal findings and key values in {target_lang} here..."
                    }}
                    Do not wrap the JSON in markdown code blocks. Just return the raw JSON object.
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=[
                            types.Part.from_bytes(
                                data=file_bytes,
                                mime_type=mime_type,
                            ),
                            prompt
                        ],
                        config={
                            "response_mime_type": "application/json"
                        }
                    )
                    
                    # Parse the structured JSON response
                    try:
                        data = json.loads(response.text.strip())
                        report.ai_summary = data.get('explanation', '')
                        report.ai_abnormal_findings = data.get('abnormal_findings', '')
                    except Exception:
                        # Fallback if parsing fails
                        report.ai_summary = response.text
                        report.ai_abnormal_findings = "Refer to the summary above for findings."
                    
                    report.save()
                    messages.success(request, f"Report '{report.title}' uploaded and analyzed successfully!")
                except Exception as e:
                    # Capture any Gemini API or file reading exceptions gracefully
                    report.ai_summary = f"Unable to generate AI summary: {str(e)}"
                    report.ai_abnormal_findings = "Summary generation failed."
                    report.save()
                    messages.warning(request, f"Report '{report.title}' uploaded, but AI summary generation failed.")
            else:
                report.ai_summary = "Gemini API key is not configured in settings."
                report.ai_abnormal_findings = "API key not found."
                report.save()
                messages.warning(request, f"Report uploaded, but AI summary could not be generated (no API key configured).")
                
            return redirect('reports_home')

        else:
            messages.error(request, "Failed to upload report. Please check the fields below.")
    else:
        form = HealthReportForm()
        
    return render(request, 'health_reports/upload.html', {'form': form})

@login_required
def report_detail(request, pk):
    """View details of a specific health report."""
    report = get_object_or_404(HealthReport, pk=pk, user=request.user)
    return render(request, 'health_reports/report_detail.html', {'report': report})

@login_required
def delete_report(request, pk):
    """Delete a health report."""
    report = get_object_or_404(HealthReport, pk=pk, user=request.user)
    if request.method == 'POST':
        title = report.title
        # Delete file from storage
        if report.file:
            report.file.delete(save=False)
        report.delete()
        messages.success(request, f"Report '{title}' deleted successfully.")
        return redirect('reports_home')
    return render(request, 'health_reports/confirm_delete.html', {'report': report})
