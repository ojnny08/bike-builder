from django.db import models

class BikeType(models.Model):
      class Slug(models.TextChoices):
          FIXED   = "fixed", "Fixed Gear"

      RULES = {
          "fixed": {
              "required": ["frame", "bottom_bracket", "crankset", "wheel", "tire", "stem", "handlebar", "seatpost", "saddle"],
              "optional": ["brake"],
          },
      }

      name = models.CharField(max_length=50)
      slug = models.SlugField(choices=Slug.choices)

      def get_rules(self):
          return self.RULES.get(self.slug, {"required": [], "optional": []})





