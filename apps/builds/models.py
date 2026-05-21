from django.conf import settings
from django.db import models

from apps.category.models import (
    BikeType,
    BottomBracket,
    Brake,
    Cassette,
    Crankset,
    Fork,
    Frame,
    FrontDerailleur,
    Handlebar,
    RearDerailleur,
    Saddle,
    Seatpost,
    Stem,
    Tire,
    Wheel,
)

_slot = dict(null=True, blank=True, on_delete=models.SET_NULL, related_name="+")


class Build(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="builds")
    bike_type = models.ForeignKey(BikeType, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Core
    frame = models.ForeignKey(Frame, **_slot)
    fork = models.ForeignKey(Fork, **_slot)

    # Drivetrain
    bottom_bracket = models.ForeignKey(BottomBracket, **_slot)
    crankset = models.ForeignKey(Crankset, **_slot)
    cassette = models.ForeignKey(Cassette, **_slot)
    rear_derailleur = models.ForeignKey(RearDerailleur, **_slot)
    front_derailleur = models.ForeignKey(FrontDerailleur, **_slot)

    # Wheels
    front_wheel = models.ForeignKey(Wheel, **_slot)
    rear_wheel = models.ForeignKey(Wheel, **_slot)
    front_tire = models.ForeignKey(Tire, **_slot)
    rear_tire = models.ForeignKey(Tire, **_slot)

    # Cockpit
    handlebar = models.ForeignKey(Handlebar, **_slot)
    stem = models.ForeignKey(Stem, **_slot)

    # Brakes
    front_brake = models.ForeignKey(Brake, **_slot)
    rear_brake = models.ForeignKey(Brake, **_slot)

    # Contact points
    saddle = models.ForeignKey(Saddle, **_slot)
    seatpost = models.ForeignKey(Seatpost, **_slot)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} — {self.name}"

    def get_compatibility_issues(self):
        """
        Returns a list of compatibility error strings.
        Empty list means the build is fully compatible.
        """
        issues = []
        f = self.frame
        fk = self.fork
        bb = self.bottom_bracket
        cs = self.crankset
        ca = self.cassette
        rd = self.rear_derailleur
        fw = self.front_wheel
        rw = self.rear_wheel
        ft = self.front_tire
        rt = self.rear_tire
        hb = self.handlebar
        st = self.stem

        if f and bb and f.bb_shell != bb.shell_type:
            issues.append(
                f"Frame BB shell ({f.bb_shell}) doesn't match bottom bracket shell ({bb.shell_type})."
            )

        if bb and cs and bb.spindle_interface != cs.spindle_interface:
            issues.append(
                f"Bottom bracket spindle ({bb.spindle_interface}) doesn't match crankset spindle ({cs.spindle_interface})."
            )

        if f and fk:
            head_to_steerer = {
                Frame.HeadTubeType.TAPERED: Fork.SteererDiameter.TAPERED,
                Frame.HeadTubeType.STRAIGHT: Fork.SteererDiameter.STRAIGHT,
            }
            if head_to_steerer.get(f.head_tube_type) != fk.steerer_diameter:
                issues.append(
                    f"Frame head tube ({f.head_tube_type}) incompatible with fork steerer ({fk.steerer_diameter})."
                )

        if f and rw:
            frame_to_wheel_axle = {
                Frame.RearAxleStandard.QR_135: Wheel.AxleStandard.QR_REAR,
                Frame.RearAxleStandard.THRU_142: Wheel.AxleStandard.THRU_REAR,
                Frame.RearAxleStandard.THRU_148: Wheel.AxleStandard.THRU_REAR_BOOST,
            }
            if frame_to_wheel_axle.get(f.rear_axle_standard) != rw.axle_standard:
                issues.append(
                    f"Frame rear axle ({f.rear_axle_standard}) incompatible with rear wheel axle ({rw.axle_standard})."
                )

        if fk and fw:
            fork_to_wheel_axle = {
                Fork.FrontAxleStandard.QR_100: Wheel.AxleStandard.QR_FRONT,
                Fork.FrontAxleStandard.THRU_100: Wheel.AxleStandard.THRU_FRONT,
                Fork.FrontAxleStandard.THRU_110: Wheel.AxleStandard.THRU_FRONT_BOOST,
            }
            if fork_to_wheel_axle.get(fk.front_axle_standard) != fw.axle_standard:
                issues.append(
                    f"Fork front axle ({fk.front_axle_standard}) incompatible with front wheel axle ({fw.axle_standard})."
                )

        if ca and rd and ca.speeds != rd.speeds:
            issues.append(
                f"Cassette ({ca.speeds}s) doesn't match rear derailleur ({rd.speeds}s)."
            )

        if fw and rw and fw.wheel_size != rw.wheel_size:
            issues.append(
                f"Front wheel size ({fw.wheel_size}) doesn't match rear wheel size ({rw.wheel_size})."
            )

        if fw and ft and fw.wheel_size != ft.wheel_size:
            issues.append(
                f"Front wheel size ({fw.wheel_size}) doesn't match front tire size ({ft.wheel_size})."
            )

        if rw and rt and rw.wheel_size != rt.wheel_size:
            issues.append(
                f"Rear wheel size ({rw.wheel_size}) doesn't match rear tire size ({rt.wheel_size})."
            )

        if f and ft and ft.width_mm > f.max_tire_clearance_mm:
            issues.append(
                f"Front tire width ({ft.width_mm}mm) exceeds frame clearance ({f.max_tire_clearance_mm}mm)."
            )

        if f and rt and rt.width_mm > f.max_tire_clearance_mm:
            issues.append(
                f"Rear tire width ({rt.width_mm}mm) exceeds frame clearance ({f.max_tire_clearance_mm}mm)."
            )

        if hb and st and hb.clamp_diameter_mm != st.bar_clamp_diameter_mm:
            issues.append(
                f"Handlebar clamp ({hb.clamp_diameter_mm}mm) doesn't match stem bar clamp ({st.bar_clamp_diameter_mm}mm)."
            )

        return issues
