from django.core.management.base import BaseCommand
from notes.models import WorkType, WorkItemDetail, WorkActivity

DATA = [
    {
        'name': 'أعمال النظافة',
        'category': 'restroom',
        'element_name': 'عام',
        'activities': [
            'أدوات النظافة',
            'مواد النظافة',
            'أعمال النظافة الدورية لدورات المياه'
        ]
    },
    {
        'name': 'أعمال الصيانة',
        'category': 'restroom',
        'element_name': 'عام',
        'activities': [
            'الاعمال المدنية',
            'الأعمال الكهربائية',
            'الأعمال الميكانيكية'
        ]
    },
]


class Command(BaseCommand):
    help = 'Seeds all work types and activities for restrooms'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting seeding of restroom work hierarchy...'))
        
        created_wt_count = 0
        created_elem_count = 0
        created_act_count = 0

        for wt_data in DATA:
            wt_name = wt_data['name']
            wt_category = wt_data['category']

            work_type, wt_created = WorkType.objects.get_or_create(
                name=wt_name,
                category=wt_category,
                defaults={'is_active': True}
            )
            if wt_created:
                created_wt_count += 1
            else:
                work_type.is_active = True
                work_type.save()

            elem_name = wt_data['element_name']
            element, elem_created = WorkItemDetail.objects.get_or_create(
                work_type=work_type,
                name=elem_name,
                defaults={'is_active': True}
            )
            if elem_created:
                created_elem_count += 1

            for act_name in wt_data['activities']:
                activity, act_created = WorkActivity.objects.get_or_create(
                    element=element,
                    name=act_name,
                    defaults={'is_active': True}
                )
                if act_created:
                    created_act_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seeding restroom completed successfully! WorkTypes: {created_wt_count}, Elements: {created_elem_count}, Activities: {created_act_count}'
        ))
