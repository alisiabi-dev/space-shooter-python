"""Basic checks that every asset configured by the game is present."""
from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from data import list_of_images, list_of_sounds  # noqa: E402


class AssetPathTests(unittest.TestCase):
    def test_all_image_paths_exist(self):
        for asset_id, image_group in list_of_images.items():
            for field, relative_path in image_group.items():
                if field.startswith("Image"):
                    with self.subTest(asset_id=asset_id, field=field):
                        self.assertTrue((PROJECT_ROOT / relative_path).is_file(), relative_path)

    def test_all_sound_paths_exist(self):
        for sound_id, sound_info in list_of_sounds.items():
            relative_path = sound_info["address"]
            with self.subTest(sound_id=sound_id):
                self.assertTrue((PROJECT_ROOT / relative_path).is_file(), relative_path)


if __name__ == "__main__":
    unittest.main()
