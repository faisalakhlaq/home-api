import tempfile
import os
from PIL import Image

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse

from apps.properties.models import Property, PropertyImage

from .test_setup import TestSetUp


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class TestPropertyWithImagesAPI(TestSetUp):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.list_url: str = reverse("apps.properties:properties-list")
        cls.detail_url: str = "apps.properties:properties-detail"
        cls.property_form_url: str = reverse(
            "apps.properties:properties-get-create-property-form-data"
        )
        cls.property_count_url: str = reverse("apps.properties:properties-count")

    def setUp(self) -> None:
        super().setUp()
        self.client.force_authenticate(user=self.user)

    def create_test_image(
        self, filename="test_image.jpg", size=(100, 100), format="JPEG"
    ):
        """Helper method to create a test image file"""
        image = Image.new("RGB", size, color="red")
        temp_file = tempfile.NamedTemporaryFile(
            suffix=f".{format.lower()}", delete=False
        )
        image.save(temp_file, format=format)
        temp_file.seek(0)

        with open(temp_file.name, "rb") as f:
            uploaded_file = SimpleUploadedFile(
                filename, f.read(), content_type=f"image/{format.lower()}"
            )

        # Clean up temp file
        os.unlink(temp_file.name)
        return uploaded_file

    def test_create_property_with_single_image(self) -> None:
        """Test property creation with a single image"""
        # Create test image
        test_image = self.create_test_image("living_room.jpg")

        # Prepare property data
        property_data = {
            **self.property_payload,
            "description": "A lovely apartment in the city center",
            "price": 250000,
            # Image data in the format your serializer expects
            "property_images[0].title": "Living Room",
            "property_images[0].description": "Spacious living room with natural light",
            "property_images[0].is_primary": "true",
            "property_images[0].image": test_image,
        }

        # Make the request
        response = self.client.post(
            self.list_url,
            data=property_data,
            format="multipart",
        )

        # Assertions
        self.assertEqual(response.status_code, 201)

        # Check property was created
        property_instance = Property.objects.get(id=response.data["id"])
        self.assertEqual(property_instance.owner, self.user)

        # Check image was created
        property_images = PropertyImage.objects.filter(property=property_instance)
        self.assertEqual(property_images.count(), 1)

        image = property_images.first()
        self.assertEqual(image.title, "Living Room")
        self.assertEqual(image.description, "Spacious living room with natural light")
        self.assertTrue(image.is_primary)
        self.assertTrue(image.image)

        # Clean up
        property_instance.delete()

    def test_create_property_with_multiple_images(self) -> None:
        """Test property creation with multiple images"""
        # Create test images
        image1 = self.create_test_image("living_room.jpg")
        image2 = self.create_test_image("bedroom.jpg")
        image3 = self.create_test_image("kitchen.png", format="PNG")

        property_data = {
            **self.property_payload,
            "description": "A beautiful villa with stunning views",
            "price": 750000,
            # Multiple images data
            "property_images[0].title": "Living Room",
            "property_images[0].description": "Main living area",
            "property_images[0].is_primary": "true",
            "property_images[1].title": "Master Bedroom",
            "property_images[1].description": "Spacious master bedroom",
            "property_images[1].is_primary": "false",
            "property_images[2].title": "Kitchen",
            "property_images[2].description": "Modern kitchen with island",
            "property_images[2].is_primary": "false",
            "property_images[0].image": image1,
            "property_images[1].image": image2,
            "property_images[2].image": image3,
        }

        response = self.client.post(
            self.list_url, data=property_data, format="multipart"
        )

        self.assertEqual(response.status_code, 201)

        property_instance = Property.objects.get(id=response.data["id"])
        property_images = PropertyImage.objects.filter(
            property=property_instance
        ).order_by("id")

        # Check we have 3 images
        self.assertEqual(property_images.count(), 3)

        # Check primary image
        primary_images = property_images.filter(is_primary=True)
        self.assertEqual(primary_images.count(), 1)
        self.assertEqual(primary_images.first().title, "Living Room")

        # Check all image titles
        titles = list(property_images.values_list("title", flat=True))
        expected_titles = ["Living Room", "Master Bedroom", "Kitchen"]
        self.assertEqual(sorted(titles), sorted(expected_titles))

        # Clean up
        property_instance.delete()

    def test_create_property_with_partial_image_data(self) -> None:
        """Test property creation where some images have missing files"""
        test_image = self.create_test_image("valid_image.jpg")

        property_data = {
            **self.property_payload,
            "description": "Testing partial image data",
            "price": 200000,
            # First image with file
            "property_images[0].title": "Valid Image",
            "property_images[0].is_primary": "true",
            # Second image without file (should be ignored)
            "property_images[1].title": "Invalid Image",
            "property_images[1].is_primary": "false",
            "property_images[0].image": test_image,
        }

        response = self.client.post(
            self.list_url, data=property_data, format="multipart"
        )

        self.assertEqual(response.status_code, 201)

        property_instance = Property.objects.get(id=response.data["id"])
        property_images = PropertyImage.objects.filter(property=property_instance)

        # Should only create the image that has a file
        self.assertEqual(property_images.count(), 1)
        self.assertEqual(property_images.first().title, "Valid Image")

        # Clean up
        property_instance.delete()

    def test_create_property_with_non_sequential_indices(self) -> None:
        """Test that non-sequential indices work correctly"""
        image1 = self.create_test_image("image1.jpg")
        image2 = self.create_test_image("image2.jpg")

        property_data = {
            **self.property_payload,
            "description": "Testing non-sequential indices",
            "price": 300000,
            # Using indices 0 and 5 (non-sequential)
            "property_images[0].title": "First Image",
            "property_images[0].is_primary": "true",
            "property_images[5].title": "Second Image",
            "property_images[5].is_primary": "false",
            "property_images[0].image": image1,
            "property_images[5].image": image2,
        }

        response = self.client.post(
            self.list_url, data=property_data, format="multipart"
        )

        self.assertEqual(response.status_code, 201)

        property_instance = Property.objects.get(id=response.data["id"])
        property_images = PropertyImage.objects.filter(property=property_instance)

        self.assertEqual(property_images.count(), 2)

        titles = list(property_images.values_list("title", flat=True))
        self.assertIn("First Image", titles)
        self.assertIn("Second Image", titles)

        # Clean up
        property_instance.delete()

    def test_create_property_image_boolean_parsing(self) -> None:
        """Test that is_primary boolean is parsed correctly from string"""
        test_image = self.create_test_image("boolean_test.jpg")

        property_data = {
            **self.property_payload,
            "description": "Testing boolean parsing",
            "price": 180000,
            "property_images[0].title": "Test Image",
            "property_images[0].is_primary": "True",  # Capital T
            "property_images[0].image": test_image,
        }

        response = self.client.post(
            self.list_url, data=property_data, format="multipart"
        )

        self.assertEqual(response.status_code, 201)

        property_instance = Property.objects.get(id=response.data["id"])
        property_image = PropertyImage.objects.get(property=property_instance)

        self.assertTrue(property_image.is_primary)

        # Clean up
        property_instance.delete()

    def test_create_property_with_large_image(self) -> None:
        """Test property creation with a larger image file"""
        # Create a larger test image
        large_image = self.create_test_image("large_image.jpg", size=(800, 600))

        property_data = {
            **self.property_payload,
            "description": "Testing with larger image",
            "price": 400000,
            "property_images[0].title": "Large Image",
            "property_images[0].is_primary": "true",
            "property_images[0].image": large_image,
        }

        response = self.client.post(
            self.list_url, data=property_data, format="multipart"
        )
        self.assertEqual(response.status_code, 201)

        property_instance = Property.objects.get(id=response.data["id"])
        property_image = PropertyImage.objects.get(property=property_instance)

        # Verify the image was saved
        self.assertTrue(property_image.image)
        self.assertTrue(property_image.image.name)

        # Clean up
        property_instance.delete()

    def tearDown(self) -> None:
        # Clean up the temporary media directory
        import shutil

        if os.path.exists(self.test_media_root):
            shutil.rmtree(self.test_media_root)

        # Restore original media root
        settings.MEDIA_ROOT = self.original_media_root
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
