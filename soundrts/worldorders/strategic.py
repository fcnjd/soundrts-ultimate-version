"""Immediate orders exposed by RMG city centres."""

from .immediate import ImmediateOrder


class _RmgCityOrder(ImmediateOrder):
    population_cost = 0

    @property
    def cost(self):
        from ..rmg_systems import menu_resource_cost

        return menu_resource_cost(self.keyword, self.unit)

    @classmethod
    def is_allowed(cls, unit, *unused_args):
        from ..rmg_systems import is_city

        return bool(
            is_city(unit)
            and getattr(getattr(unit, "world", None), "rmg_strategic_systems", False)
        )

    def _target(self):
        if not self.args:
            return None
        return self.player.get_object_by_id(self.args[0])

    def _finish(self, success):
        if success:
            self.unit.notify("order_ok")
            from ..rmg_systems import announce_strategic_order_success

            announce_strategic_order_success(self.player, self.keyword)
        else:
            self.unit.notify("order_impossible")


class RmgBuyTileOrder(_RmgCityOrder):
    keyword = "rmg_buy_tile"
    nb_args = 1

    def immediate_action(self):
        from ..rmg_systems import buy_tile

        self._finish(buy_tile(self.player, self.unit, self._target()))


class _RmgAssignOrder(_RmgCityOrder):
    nb_args = 1
    focus = ""

    def immediate_action(self):
        from ..rmg_systems import assign_citizen

        self._finish(
            assign_citizen(self.player, self.unit, self._target(), self.focus)
        )


class RmgAssignGoldOrder(_RmgAssignOrder):
    keyword = "rmg_assign_gold"
    focus = "gold"


class RmgAssignWoodOrder(_RmgAssignOrder):
    keyword = "rmg_assign_wood"
    focus = "wood"


class RmgAssignFoodOrder(_RmgAssignOrder):
    keyword = "rmg_assign_food"
    focus = "food"


class RmgAssignCultureOrder(_RmgAssignOrder):
    keyword = "rmg_assign_culture"
    focus = "culture"


class _RmgPolicyOrder(_RmgCityOrder):
    nb_args = 0
    policy = ""

    @classmethod
    def is_allowed(cls, unit, *unused_args):
        if not super().is_allowed(unit):
            return False
        from ..rmg_systems import initialize_player

        initialize_player(unit.player)
        return (
            cls.policy in unit.player.rmg_unlocked_policies
            and cls.policy not in unit.player.rmg_policy_slots
        )

    def immediate_action(self):
        from ..rmg_systems import switch_policy

        self._finish(switch_policy(self.player, self.policy))


class RmgSwitchTraditionOrder(_RmgPolicyOrder):
    keyword = "rmg_switch_tradition"
    policy = "rmg_policy_tradition"


class RmgSwitchCommerceOrder(_RmgPolicyOrder):
    keyword = "rmg_switch_commerce"
    policy = "rmg_policy_commerce"


class RmgSwitchDiplomacyOrder(_RmgPolicyOrder):
    keyword = "rmg_switch_diplomacy"
    policy = "rmg_policy_diplomacy"
