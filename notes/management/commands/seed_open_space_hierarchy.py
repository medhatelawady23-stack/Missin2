from django.core.management.base import BaseCommand
from notes.models import WorkType, WorkItemDetail, WorkActivity

DATA = [
    {
        'name': 'أعمال النظافة',
        'category': 'open_space',
        'elements': [
            {
                'name': 'الموقع',
                'activities': ['النظافة العامة للموقع']
            },
            {
                'name': 'غرف المضخات',
                'activities': ['نظافة غرفة المضخات']
            },
            {
                'name': 'المنشآت المائية',
                'activities': ['نظافة المنشآت المائية']
            },
        ]
    },
    {
        'name': 'الأعمال الزراعية',
        'category': 'open_space',
        'elements': [
            {
                'name': 'المسطحات الخضراء',
                'activities': [
                    'قص وتحديد',
                    'تعشيب',
                    'إستبدال الميت والمفقود',
                    'تسميد وتهوية التربة'
                ]
            },
            {
                'name': 'غطائيات التربة',
                'activities': [
                    'قص وتحديد',
                    'إستبدال الميت والمفقود',
                    'تعشيب',
                    'التسميد'
                ]
            },
            {
                'name': 'النخيل',
                'activities': [
                    'تكريب النخيل وإزالة الفسائل الأرضية والهوائية',
                    'تعشيب وشقرفة وإزالة التربة الزائدة في الاحواض',
                    'إستبدال الميت والمفقود',
                    'إزالة السعف الجاف وصرم النخيل وتنظيف الثمار',
                    'التسميد العضوي والكيماوي'
                ]
            },
            {
                'name': 'الأشجار',
                'activities': [
                    'تربية وتقليم الأشجار وتنظيف الساق من النموات الجانبية',
                    'تسميد',
                    'تسنيد وتدعيم الأشجار',
                    'إستبدال الميت والمفقود',
                    'تعشيب وشقرفة وإزالة التربة الزائدة في الاحواض'
                ]
            },
            {
                'name': 'الشجيرات والأسيجة',
                'activities': [
                    'قص وتشكيل الأسيجة والشجيرات الفردية',
                    'تسميد',
                    'إستبدال الميت والمفقود',
                    'تسنيد وتدعيم الشجيرات الفردية',
                    'تعشيب وشقرفة وإزالة التربة الزائدة في الاحواض'
                ]
            },
            {
                'name': 'الزهور والحوليات',
                'activities': [
                    'تجهيز الاحواض لزراعة الحوليات والزهور',
                    'تنسيق الزراعة بشكل جمالي ومنظم',
                    'إستبدال الميت والمفقود',
                    'تعشيب وشقرفة',
                    'التسميد'
                ]
            },
            {
                'name': 'المكافحة والوقاية',
                'activities': [
                    'المكافحة الكيميائية للآفات الحشرية والفطرية والأعشاب',
                    'استخدام مبيدات الصحة العامة في المواقع التي تحتاج ذلك'
                ]
            },
        ]
    },
    {
        'name': 'الاعمال المدنية',
        'category': 'open_space',
        'elements': [
            {
                'name': 'الأحواض',
                'activities': [
                    'صيانة البردورات والأحواض الزراعية'
                ]
            },
            {
                'name': 'الخزانات وغرف المضخات',
                'activities': [
                    'صيانة ونظافة خزانات الري',
                    'صيانة أغطية الخزانات',
                    'علاج التشققات والتصدعات',
                    'عزل الجدران والارضيات والأسقف لغرف المضخات'
                ]
            },
            {
                'name': 'المنشآت المائية',
                'activities': [
                    'تغيير مياه النافورة',
                    'إضافة الكيماويات الي مياه النافورة للحفاظ علي نظافة المياه',
                    'كسوة مبني المنشأة المائية من الرخام والجرانيت والسيراميك ...',
                    'الالتزام بجدول التشغيل المعتمد من الجهات الاشرافية'
                ]
            },
        ]
    },
    {
        'name': 'الأعمال الكهربائية',
        'category': 'open_space',
        'elements': [
            {
                'name': 'شبكة الإنارة',
                'activities': [
                    'مراجعة اللمبات واستبدال ا التالف والمفقود مع مراعاة توحيد اللون'
                ]
            },
            {
                'name': 'اللوحات الكهربائية',
                'activities': [
                    'تنظيم الكابلات المغذية لللوحات في حامل الكابلات',
                    'صيانة ونظافة اللوحات الكهربائية بأنواعها'
                ]
            },
            {
                'name': 'مراوح الشفط',
                'activities': [
                    'صيانة أو إستبدال مراوح الشفط التالفة والمفقودة'
                ]
            },
            {
                'name': 'التوصيلات والكابلات',
                'activities': [
                    'تأمين جميع التوصيلات والكابلات ( أمن وسلامة )'
                ]
            },
        ]
    },
    {
        'name': 'الأعمال الميكانيكية والري',
        'category': 'open_space',
        'elements': [
            {
                'name': 'الآبار',
                'activities': [
                    'صيانة ونظافة غرفة البئر',
                    'صيانة مضخات الآبار'
                ]
            },
            {
                'name': 'المضخات',
                'activities': [
                    'صيانة وتشحيم مضخات الري',
                    'صيانة وغسيل الفلاتر',
                    'صيانة أسطوانات و عدادات الضغط',
                    'صيانة المضخات الغاطسة ( أمن وسلامة )'
                ]
            },
            {
                'name': 'المنشآت المائية',
                'activities': [
                    'صيانة وتشحيم مضخات النوافير',
                    'صيانة أسطوانات الضغط',
                    'صيانة عدادات الضغط',
                    'تمديدات وفوهات النوافير'
                ]
            },
            {
                'name': 'طفاية الحريق',
                'activities': [
                    'صيانة أو إستبدال طفايات الحريق ( أمن وسلامة )'
                ]
            },
        ]
    },
    {
        'name': 'اعمال الري',
        'category': 'open_space',
        'elements': [
            {
                'name': 'الري',
                'activities': [
                    'صيانة خطوط الري الرئيسية والفرعية والليات وتثبيتها',
                    'صيانة المحابس وصناديق المحابس وإستبدال التالف وإضافة الحصى',
                    'صيانة الرشاشات والبيبلرات والنقاطات',
                    'منع تسريبات وخروج مياه الري خارج الأحواض والمزروعات',
                    'ري جميع المزروعات بكميات مياه كافية'
                ]
            },
        ]
    },
]


class Command(BaseCommand):
    help = 'Seeds all work types, elements, and activities for open spaces'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting seeding of open_space work hierarchy...'))
        
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

            for elem_data in wt_data['elements']:
                elem_name = elem_data['name']
                element, elem_created = WorkItemDetail.objects.get_or_create(
                    work_type=work_type,
                    name=elem_name,
                    defaults={'is_active': True}
                )
                if elem_created:
                    created_elem_count += 1

                for act_name in elem_data['activities']:
                    activity, act_created = WorkActivity.objects.get_or_create(
                        element=element,
                        name=act_name,
                        defaults={'is_active': True}
                    )
                    if act_created:
                        created_act_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seeding open_space completed successfully! WorkTypes: {created_wt_count}, Elements: {created_elem_count}, Activities: {created_act_count}'
        ))
