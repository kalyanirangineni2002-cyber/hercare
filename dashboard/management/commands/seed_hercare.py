from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from appointments.models import Doctor, TimeSlot
from nutrition.models import NutritionArticle, FitnessRoutine, DailyTip
from mental_health.models import CounselingResource
import datetime

class Command(BaseCommand):
    help = 'Pre-seeds the database with realistic sample health and medical records'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Clearing existing seed data..."))
        
        # Clear existing models (sample data only, to prevent duplication)
        Doctor.objects.all().delete()
        NutritionArticle.objects.all().delete()
        FitnessRoutine.objects.all().delete()
        DailyTip.objects.all().delete()
        CounselingResource.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS("Existing seed data cleared."))
        
        # 1. Seed Specialized Doctors
        self.stdout.write("Seeding specialized doctors...")
        doctors_data = [
            {
                'name': 'Sarah Jenkins',
                'specialization': 'gynecologist',
                'qualification': 'MD, OB-GYN, Fellowship in Reproductive Endocrinology',
                'experience_years': 14,
                'rating': 4.9,
                'consultation_fee': 1500.00,
                'bio': 'Dr. Sarah Jenkins is an expert in women\'s reproductive wellness, specialized in menstrual cycle disorders, PCOS/PCOD management, and hormonal therapies. She has published multiple papers on holistic endocrine wellness.',
                'available_days': 'Mon,Tue,Wed,Thu,Fri',
            },
            {
                'name': 'Priya Sharma',
                'specialization': 'nutritionist',
                'qualification': 'M.Sc in Clinical Nutrition & Dietetics, Certified Diabetes Educator',
                'experience_years': 9,
                'rating': 4.8,
                'consultation_fee': 1000.00,
                'bio': 'Dr. Priya Sharma specializes in therapeutic diets, women\'s physical fitness, hormonal balancing menus, and tailored nutritional programs for metabolic health, including Thyroid and PCOD diets.',
                'available_days': 'Mon,Wed,Fri,Sat',
            },
            {
                'name': 'Evelyn Vance',
                'specialization': 'endocrinologist',
                'qualification': 'MD, DM - Endocrinology, FACP (USA)',
                'experience_years': 18,
                'rating': 4.9,
                'consultation_fee': 1800.00,
                'bio': 'Dr. Evelyn Vance is a globally renowned specialist in hormonal dysfunction, reproductive medicine, and insulin resistance. She has spent nearly two decades treating complex thyroid and metabolic disorders.',
                'available_days': 'Tue,Wed,Thu',
            },
            {
                'name': 'Elena Rostova',
                'specialization': 'psychologist',
                'qualification': 'Ph.D. in Clinical Psychology, Cognitive Behavioral Specialist',
                'experience_years': 11,
                'rating': 4.7,
                'consultation_fee': 1200.00,
                'bio': 'Dr. Elena Rostova provides counseling and mindfulness therapies. She specializes in stress management, anxiety relief, emotional coping techniques, and mindfulness workshops tailored for women.',
                'available_days': 'Mon,Tue,Thu,Fri',
            }
        ]
        
        doctors = []
        for d_info in doctors_data:
            doc = Doctor.objects.create(**d_info)
            doctors.append(doc)
            self.stdout.write(self.style.SUCCESS(f"  Created Doctor: Dr. {doc.name}"))
            
        # 2. Seed Time Slots for the next 6 days
        self.stdout.write("Generating available consultation timeslots for the next 6 days...")
        today = datetime.date.today()
        slots_data = [
            (datetime.time(10, 0), datetime.time(10, 45)),
            (datetime.time(11, 30), datetime.time(12, 15)),
            (datetime.time(14, 0), datetime.time(14, 45)),
            (datetime.time(16, 30), datetime.time(17, 15)),
        ]
        
        slot_count = 0
        for i in range(6):
            target_date = today + datetime.timedelta(days=i)
            day_str = target_date.strftime('%a') # Mon, Tue, etc.
            
            for doc in doctors:
                # Check if this day is in doctor's available days
                if day_str in doc.available_days:
                    for start_t, end_t in slots_data:
                        TimeSlot.objects.create(
                            doctor=doc,
                            date=target_date,
                            start_time=start_t,
                            end_time=end_t,
                            is_booked=False
                        )
                        slot_count += 1
                        
        self.stdout.write(self.style.SUCCESS(f"  Generated {slot_count} consultation slots successfully."))

        # 3. Seed Nutrition Articles
        self.stdout.write("Seeding nutrition and fitness articles...")
        articles_data = [
            {
                'title': 'The Ultimate PCOS & PCOD Diet Blueprint',
                'category': 'pcos',
                'summary': 'Learn the core principles of an anti-inflammatory insulin-sensitizing diet to naturally regulate cycles and manage PCOS.',
                'content': """Polycystic Ovary Syndrome (PCOS) affects 1 in 10 women of childbearing age. An effective diet is one of the most powerful tools to manage insulin resistance and hormonal balance.

### Key Dietary Strategies:
1. **Prioritize Low-Glycemic Index (GI) Carbohydrates:** Foods like oats, quinoa, brown rice, and legumes digest slowly, preventing rapid blood sugar spikes.
2. **Increase Lean Protein Intake:** Including high-quality protein (greek yogurt, eggs, lentils, lean poultry) in every meal helps stabilize glucose levels and reduces sweet cravings.
3. **Incorporate Anti-inflammatory Fats:** Omega-3 rich foods like walnuts, flaxseeds, chia seeds, and extra virgin olive oil reduce systemic inflammation and support follicular health.
4. **Load up on Fiber:** Fiber binds to excess hormones in the gut, aiding detoxification. Eat plenty of broccoli, Brussels sprouts, kale, and berries.
5. **Ditch Refined Sugars:** High intake of artificial sweets triggers insulin spikes, driving excess androgen production (leading to acne and hirsutism).

Focus on consistent, whole-food nutrition and mindful eating to reclaim your hormonal health!""",
                'tags': 'PCOS, Hormones, Insulin Resistance, Nutrition',
                'is_featured': True,
            },
            {
                'title': 'Thyroid Health: Nutrients Your Thyroid Needs',
                'category': 'hormonal',
                'summary': 'Struggling with hypothyroidism or sluggish metabolism? Discover the essential vitamins and minerals that boost thyroid conversion.',
                'content': """Your thyroid gland requires highly specific trace elements to produce thyroid hormones (T4 and T3). Here are the primary minerals and nutrients you should focus on:

### 1. Selenium
Selenium is a vital antioxidant and co-factor for the enzyme that converts T4 (inactive thyroid hormone) to T3 (active thyroid hormone).
* **Top sources:** Brazil nuts (just 2 a day provides 100% RDA!), sunflower seeds, mushrooms, and fish.

### 2. Iodine
Iodine is the literal building block of thyroid hormone molecules.
* **Top sources:** Iodized salt, seaweeds (like kelp or nori), dairy, and eggs. *Note: Avoid excessive supplementation if you have Hashimoto's thyroiditis.*

### 3. Zinc
Zinc plays a critical role in thyroid hormone synthesis and receptor binding.
* **Top sources:** Pumpkin seeds, chickpeas, oysters, and spinach.

### 4. Iron
Iron deficiency directly impairs thyroid peroxidase (TPO) activity, leading to reduced hormone synthesis.
* **Top sources:** Dark leafy greens, lentils, beans, and lean red meats. Combine with Vitamin C (citrus fruits) to boost absorption!""",
                'tags': 'Thyroid, Hormones, Sluggish Metabolism, Minerals',
                'is_featured': True,
            },
            {
                'title': 'Healthy Recipe: Avocado & Chickpea Power Salad',
                'category': 'recipes',
                'summary': 'A delicious, high-fiber, high-protein recipe loaded with healthy fats to keep you energized all afternoon.',
                'content': """Looking for a quick, nutrient-dense lunch that doesn't trigger a 3 PM energy crash? This Avocado & Chickpea Power Salad is packed with filling fiber, heart-healthy fats, and clean protein.

### Ingredients:
* 1 can chickpeas (garbanzo beans), drained and rinsed
* 1 ripe Hass avocado, cubed
* 1 cup cherry tomatoes, halved
* 1 cucumber, diced
* 1/4 cup red onion, finely chopped
* 1/4 cup crumbled feta cheese (optional)
* Handful of fresh cilantro or parsley

### For the Dressing:
* 2 tablespoons extra virgin olive oil
* Juice of 1 freshly squeezed lemon
* 1 clove garlic, minced
* Salt and black pepper to taste

### Instructions:
1. **Prepare the Veg:** Toss the chickpeas, diced avocado, halved cherry tomatoes, chopped cucumber, and red onion into a large bowl.
2. **Whisk the Dressing:** In a small bowl, whisk the olive oil, lemon juice, minced garlic, salt, and pepper until emulsified.
3. **Assemble:** Pour the dressing over the salad and toss gently to avoid mashing the avocado.
4. **Garnish:** Top with crumbled feta cheese and fresh herbs. Serve immediately or store in the fridge for up to 24 hours.""",
                'tags': 'Recipes, Fiber, Plant Protein, Healthy Lunch',
                'is_featured': False,
            },
            {
                'title': 'Hydration Hacks for Optimal Cellular Energy',
                'category': 'hydration',
                'summary': 'Simple habits to ensure your body is fully hydrated, boosting skin quality, digestion, and fatigue relief.',
                'content': """Hydration is about more than just drinking 8 glasses of plain water. True hydration involves mineral absorption at a cellular level, which maintains blood volume, brain function, and digestive speed.

### Cellular Hydration Tips:
* **Add a Pinch of Sea Salt:** A tiny pinch of high-quality unrefined salt in your morning glass of water replenishes trace minerals (electrolytes) for better cellular uptake.
* **Eat Your Water:** Eat cucumbers, watermelon, celery, and strawberries. The water in raw vegetables is structurally structured and absorbed slowly.
* **Limit Diuretics:** Excessive black coffee, tea, and sugary energy drinks flush minerals out of your body, causing dehydration even if you drink lots of liquids.
* **Track by Urine Color:** Strive for a pale, straw-like yellow color. If it\'s dark gold, you\'re dehydrated; if it\'s completely clear, you might be flushing electrolytes.""",
                'tags': 'Hydration, Wellness, Energy, Skin Health',
                'is_featured': False,
            },
            {
                'title': 'Weight Management: The Metabolic Flexibility Method',
                'category': 'weight',
                'summary': 'Understand metabolic flexibility—how your body switches fuels—to naturally manage weight without crash diets.',
                'content': """Metabolic flexibility is your body's ability to easily switch between burning carbohydrates (glucose) and burning fat for energy. 

### Why is this important?
Crash diets slow down your basal metabolic rate, causing quick weight regain. Training metabolic flexibility helps preserve muscle mass and naturally burns fat reserves.

### How to Improve Metabolic Flexibility:
1. **Practice Intermittent Rest:** Allow a clean 12 to 14-hour overnight fasting window (e.g., dinner at 7 PM, breakfast at 9 AM) to encourage your body to tap into stored glycogen.
2. **Incorporate Strength Training:** Building lean muscle tissue provides a larger metabolic sink for absorbing glucose, reducing insulin resistance.
3. **Reduce Constant Snacking:** Eating every 2 hours keeps insulin chronically elevated, keeping your body in "fat storage mode" instead of "fat burning mode".""",
                'tags': 'Weight, Metabolism, Fat Loss, Strength',
                'is_featured': False,
            }
        ]
        
        for a_info in articles_data:
            art = NutritionArticle.objects.create(**a_info)
            self.stdout.write(self.style.SUCCESS(f"  Created Article: {art.title}"))

        # 4. Seed Fitness Routines
        self.stdout.write("Seeding fitness and exercise routines...")
        routines_data = [
            {
                'title': 'Pelvic Floor Strengthening & Core Stability',
                'difficulty': 'beginner',
                'target_area': 'pelvic',
                'duration_minutes': 20,
                'description': 'A gentle beginner-friendly routine focusing on pelvic floor activation (Kegels), deep core stabilizer engagement, and posture control.',
                'exercises': """1. **Deep Diaphragmatic Breathing** (5 minutes)
   - Relax your body, inhale deeply through your nose expanding your ribs, exhale fully drawing your navel in.
2. **Kegel Holds** (3 sets of 10 repetitions)
   - Contract your pelvic floor muscles, hold for 5 seconds, relax completely for 5 seconds.
3. **Pelvic Tilts** (3 sets of 12 reps)
   - Lie on your back, knees bent. Exhale and tilt your pelvis back, pressing your lower back into the floor.
4. **Glute Bridges** (3 sets of 10 reps)
   - Squeeze your glutes and lift your hips until your body is in a straight line. Lower slowly.""",
                'calories_burned': 120
            },
            {
                'title': 'Vinyasa Flow Yoga for Hormonal Harmony',
                'difficulty': 'intermediate',
                'target_area': 'yoga',
                'duration_minutes': 30,
                'description': 'A restorative flow blending stretching, hip opening, and thyroid stimulation to restore balance, calm the nervous system, and improve circulation.',
                'exercises': """1. **Cat-Cow Stretch** (2 minutes)
   - Mobilize spine and stimulate core.
2. **Downward Facing Dog** (3 minutes)
   - Release tension in hamstrings and back.
3. **Cobra Pose (Bhujangasana)** (5 sets of 30-second holds)
   - Stimulates the thyroid gland and opens the chest.
4. **Bridge Pose (Setu Bandhasana)** (3 sets of 1-minute holds)
   - Inversion that improves blood flow to the endocrine glands.
5. **Savasana (Corpse Pose)** (5 minutes)
   - Total relaxation and nervous system reset.""",
                'calories_burned': 150
            },
            {
                'title': 'Full Body Metabolic Blast',
                'difficulty': 'advanced',
                'target_area': 'full_body',
                'duration_minutes': 45,
                'description': 'High-intensity interval strength circuit designed to build functional muscle strength, elevate metabolic rate, and improve cardiovascular fitness.',
                'exercises': """1. **Bodyweight Squats** (4 sets of 15 reps)
2. **Dumbbell Row / Pushups** (4 sets of 12 reps)
3. **Reverse Lunges** (3 sets of 12 reps per leg)
4. **Plank Holds** (3 sets of 1 minute)
5. **Burpees or Mountain Climbers** (3 sets of 45 seconds work, 15 seconds rest)""",
                'calories_burned': 380
            }
        ]
        
        for r_info in routines_data:
            routine = FitnessRoutine.objects.create(**r_info)
            self.stdout.write(self.style.SUCCESS(f"  Created Routine: {routine.title}"))

        # 5. Seed Daily Tips
        self.stdout.write("Seeding daily health tips...")
        tips_data = [
            {
                'tip_text': 'Start your day with a glass of warm water and a squeeze of fresh lemon to support digestion, activate liver enzymes, and promote mineral uptake.',
                'category': 'nutrition'
            },
            {
                'tip_text': 'Stretching your hip flexors for just 5 minutes before bed relieves physical stress and stimulates blood flow to reproductive and lower back areas, improving sleep depth.',
                'category': 'fitness'
            },
            {
                'tip_text': 'Mindful box breathing (inhale 4s, hold 4s, exhale 4s, hold 4s) for just 3 cycles acts as an instant reboot for your sympathetic nervous system, lowering cortisol.',
                'category': 'wellness'
            },
            {
                'tip_text': 'Schedule minor tech-free breaks. A 20-minute walk in nature without your smartphone lowers psychological stress, regulates circadian rhythm, and enhances focus.',
                'category': 'mental_health'
            }
        ]
        
        for t_info in tips_data:
            tip = DailyTip.objects.create(**t_info)
            self.stdout.write(self.style.SUCCESS(f"  Created Daily Tip: {tip.tip_text[:40]}..."))

        # 6. Seed Mental Health Counseling Resources
        self.stdout.write("Seeding mental health counseling resources...")
        resources_data = [
            {
                'title': 'A Comprehensive Guide to Anxiety Relief',
                'category': 'anxiety',
                'resource_type': 'guide',
                'summary': 'Understand the psychological mechanisms of anxiety and build a custom toolkit of actionable distress tolerance and grounding techniques.',
                'content': """Anxiety is your body's survival mechanism firing at the wrong time. Understanding how the autonomic nervous system responds to stress allows you to regain control over anxious thoughts.

### Practical Grounding Exercises:
* **The 5-4-3-2-1 Technique:** Identify 5 things you can see, 4 things you can touch, 3 things you can hear, 2 things you can smell, and 1 thing you can taste. This pulls your mind out of catastrophic future loops back into the concrete present.
* **Progressive Muscle Relaxation (PMR):** Systematically tense and release every muscle group from your toes to your forehead. This discharges muscular tension and signals safety to the brain.
* **Cognitive Reframing:** Challenge catastrophic thoughts by asking: *Is this thought a factual certainty, or a hypothetical fear?* Reframe "What if I fail?" into "Even if it gets difficult, I have the skills to adapt." """,
                'is_featured': True,
            },
            {
                'title': 'Deep Stress Balance and Cortisol Reset',
                'category': 'stress',
                'resource_type': 'exercise',
                'summary': 'Learn the connection between chronic daily stress and high cortisol levels, and complete our deep nervous system reset exercise.',
                'content': """Chronic daily stressors keep our cortisol levels elevated. When cortisol remains elevated, it disrupts sleep, metabolic functions, and reproductive hormones.

### 10-Minute Cortisol Reset Protocol:
1. **Create Sanctuary:** Find a quiet room, dim the lights, and lie down comfortably.
2. **Elevate Your Legs:** Rest your legs on a chair or flat against a wall. This physical shift activates the vagus nerve.
3. **Double-Inhale Breathing:** Inhale deeply through your nose, take a second quick sniff to fully expand your lungs, then let out a slow, long sigh through your mouth. Repeat for 5 minutes.
4. **Somatic Scan:** Scan your jaw, shoulders, and belly. Actively release any clenched muscles.""",
                'is_featured': True,
            },
            {
                'title': 'Intro to Mindfulness and Somatic Awareness',
                'category': 'mindfulness',
                'resource_type': 'article',
                'summary': 'Start your mindfulness practice today. Explore simple sensory habits to stay rooted and calm throughout a hectic workday.',
                'content': """Mindfulness isn't about clearing your head of all thoughts—it's simply observing your present experience without judgment. It shifts your brain activation from the emotional amygdala to the rational prefrontal cortex.

### Simple Everyday Mindfulness Habits:
* **Sipping Meditation:** When drinking your morning tea or coffee, focus entirely on the warmth of the mug, the rising aroma, and the flavor profile of each sip. Avoid checking your phone!
* **Active Listening:** In your next conversation, listen purely to understand, rather than planning your response. Notice the speaker\'s tone, pauses, and expression.
* **Red Light Breathing:** Use moments of waiting (red lights, elevators, web pages loading) as positive cues to take three deep, slow diaphragmatic breaths.""",
                'is_featured': False,
            },
            {
                'title': 'Sleep Health: Optimize Your Circadian Rhythm',
                'category': 'sleep',
                'resource_type': 'guide',
                'summary': 'Sleep is the cornerstone of mental resilience and hormonal balance. Discover how to align your lifestyle with your sleep clock.',
                'content': """Quality sleep is essential for brain detoxification, memory consolidation, and hormone production.

### Essential Sleep Hygiene Blueprint:
* **Morning Sunlight Exposure:** Step outside within 30 minutes of waking for 10-15 minutes. This triggers cortisol release (waking you up) and sets a timer for melatonin release 16 hours later.
* **Block Blue Light:** Avoid screens (smartphones, laptops, TVs) for at least 1 hour before bedtime. Blue light tricks your brain into thinking it's midday, suppressing melatonin production.
* **Cool Room Temperature:** Your body needs to drop its core temperature by 1-2 degrees to fall asleep. Keep your bedroom cool (around 18-20°C).
* **Consistent Wake Time:** Wake up at the exact same time every day, even on weekends. This locks in your circadian phase, making it easier to fall asleep at night.""",
                'is_featured': False,
            }
        ]
        
        for res_info in resources_data:
            res = CounselingResource.objects.create(**res_info)
            self.stdout.write(self.style.SUCCESS(f"  Created Counseling Resource: {res.title}"))

        self.stdout.write(self.style.SUCCESS("\nHER CARE+ pre-seed command completed successfully!"))
