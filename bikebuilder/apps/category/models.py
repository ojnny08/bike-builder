from django.db import models

class BikeType(models.Model):
      class Slug(models.TextChoices):
          FIXED       = "fixed",       "Fixed Gear"
          ROAD_GRAVEL = "road-gravel", "Road & Gravel"
          MOUNTAIN    = "mountain",    "Mountain"

      RULES = { 
          "fixed": {
              "required": ["frame", "bottom_bracket", "crank", "wheels", "sprocket",
                           "chain", "tire", "stem", "handlebar", "seatpost", "saddle"],
              "optional": ["brake"],
              "groups": {
                  "crank": {"label": "Crank", "default": "crankset", "modes": {
                      "crankset": {"required": ["crankset"]},
                      "custom":   {"required": ["crank_arm", "chainring"],
                                   "prerequisites": {"chainring": "crank_arm"}},
                  }},
                  "wheels": {"label": "Wheels", "default": "wheelset", "modes": {
                      "wheelset": {"required": ["wheelset"], "optional": ["track_hub"],
                                   "prerequisites": {"track_hub": "wheelset"}},
                      "single":   {"required": ["wheel"]},
                      "custom":   {"required": ["rim", "track_hub"],
                                   "prerequisites": {"track_hub": "rim"}},
                  }},
              },
              "prerequisites": {
                  "bottom_bracket": "frame",
                  "crank":          "bottom_bracket",
                  "wheels":         "frame",
                  "sprocket":       "wheels",
                  "chain":          "sprocket",
                  "tire":           "wheels",
                  "handlebar":      "stem",
              },
          },
          "road-gravel": {
              "required": ["frame", "bottom_bracket", "crankset", "wheel", "sprocket", "chain", "tire", "stem", "handlebar", "seatpost", "saddle"],
              "optional": ["brake"],
          },
          "mountain": {
              "required": ["frame", "bottom_bracket", "crankset", "wheel", "sprocket", "chain", "tire", "stem", "handlebar", "seatpost", "saddle"],
              "optional": ["brake"],
          },
      }

      name = models.CharField(max_length=50)
      slug = models.SlugField(choices=Slug.choices)

      def get_rules(self):
          return self.RULES.get(self.slug, {"required": [], "optional": []})





