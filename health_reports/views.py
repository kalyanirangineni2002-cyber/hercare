from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import HealthReport
from .forms import HealthReportForm

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
            messages.success(request, f"Report '{report.title}' uploaded successfully!")
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
