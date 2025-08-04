from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from MenuApp.menu_app.models import Item

class Command(BaseCommand):
    help = 'Creates sample menu items for testing'

    def handle(self, *args, **options):
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com'}
        )
        
        # Sample menu items
        sample_items = [
            {
                'meal': 'Bruschetta',
                'description': 'Toasted bread topped with tomatoes, garlic, and fresh basil',
                'price': 8.99,
                'meal_type': 'starters',
                'status': 1,
                'image': None  # Will be added via admin interface
            },
            {
                'meal': 'Caesar Salad',
                'description': 'Fresh romaine lettuce with Caesar dressing, croutons, and parmesan cheese',
                'price': 12.99,
                'meal_type': 'salads',
                'status': 1,
                'image': None
            },
            {
                'meal': 'Grilled Salmon',
                'description': 'Fresh Atlantic salmon grilled to perfection with seasonal vegetables',
                'price': 24.99,
                'meal_type': 'main_dishes',
                'status': 1,
                'image': None
            },
            {
                'meal': 'Beef Tenderloin',
                'description': '8oz tenderloin steak with garlic mashed potatoes and asparagus',
                'price': 32.99,
                'meal_type': 'main_dishes',
                'status': 1,
                'image': None
            },
            {
                'meal': 'Tiramisu',
                'description': 'Classic Italian dessert with coffee-soaked ladyfingers and mascarpone cream',
                'price': 9.99,
                'meal_type': 'desserts',
                'status': 1,
                'image': None
            },
            {
                'meal': 'Chocolate Lava Cake',
                'description': 'Warm chocolate cake with molten center, served with vanilla ice cream',
                'price': 11.99,
                'meal_type': 'desserts',
                'status': 0,  # Unavailable
                'image': None
            }
        ]
        
        # Create items
        for item_data in sample_items:
            item, created = Item.objects.get_or_create(
                meal=item_data['meal'],
                defaults={
                    'description': item_data['description'],
                    'price': item_data['price'],
                    'meal_type': item_data['meal_type'],
                    'author': admin_user,
                    'status': item_data['status'],
                    'image': item_data['image']
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created menu item: {item.meal}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Menu item already exists: {item.meal}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Sample data creation completed!')
        )
        self.stdout.write(
            self.style.WARNING('Note: Images can be added via the admin interface at /admin/')
        ) 