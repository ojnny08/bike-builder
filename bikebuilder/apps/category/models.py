from django.db import models

class BikeType(models.Model):
      class Slug(models.TextChoices):
          FIXED   = "fixed", "Fixed Gear"

      RULES = {
          "fixed": {
              "required": ["frame", "bottom_bracket", "crankset", "wheel", "sprocket", "chain", "tire", "stem", "handlebar", "seatpost", "saddle"],
              "optional": ["brake"],
              "prerequisites": {
                  "bottom_bracket": "frame",
                  "crankset": "bottom_bracket",
                  "wheel": "frame",
                  "sprocket": "wheel",
                  "chain": "sprocket",
                  "tire": "wheel",
                  "handlebar": "stem",
              },
          },
      }

      name = models.CharField(max_length=50)
      slug = models.SlugField(choices=Slug.choices)

      def get_rules(self):
          return self.RULES.get(self.slug, {"required": [], "optional": []})





