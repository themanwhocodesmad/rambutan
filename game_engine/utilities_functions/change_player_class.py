# In views.py or a separate services.py file
def change_player_class(user_profile, new_class):
    if new_class not in user_profile.PLAYER_CLASS_CHOICES:
        return False, "Invalid class choice"

    if user_profile.class_changes >= 3:
        return False, "Maximum class changes reached"

    user_profile.player_class = new_class
    user_profile.special_troops = user_profile.PLAYER_CLASS_CHOICES[new_class]
    user_profile.class_changes += 1
    user_profile.save()

    return True, "Player class changed successfully"
