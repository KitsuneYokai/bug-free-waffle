#!/usr/bin/env python
# coding: utf-8

# ## osumapper #4: New Map Reader
# 

# Set the input file string to a timed (having the right BPM/offset) .osu file.
# 
# It converts the map/music to Python readable format.

# In[113]:


#from act_newmap_prep import *

# input file here! (don't remove the "r" before string)
# file_path = r'..\..\test_data\test.osu'

# Or use auto timing with music file only!!

from act_timing import *;
music_path = r"\test_data\audio.mp3"
file_path = get_timed_osu_file(music_path, game_mode=0);

step4_read_new_map(file_path);


# ## osumapper #5: Rhythm Predictor
# 
# Calculates a map's rhythm based on the music and timing.

# Parameters:
# 
# "note_density" determines how many notes will be placed on the timeline, ranges from 0 to 1.<br>
# "slider_favor" determines how the model favors sliders against circles, ranges from -1 to 1.<br>
# "dist_multiplier" determines the distance snap. ranges from 0 to +∞. Of course 0/+∞ are not advisable.<br>
# "divisor_favor" determines how the model favors notes to be on X divisors starting from a beat (white, blue, red, blue), ranges from -1 to 1 each.<br>
# "slider_max_ticks" determines the max amount of time a slider can slide, ranges from 1 to +∞.

# In[114]:


from act_rhythm_calc import *

model = step5_load_model();
npz = step5_load_npz();
params = step5_set_params(dist_multiplier=1, note_density=0.75, slider_favor=0.1, divisor_favor=[0] * 4, slider_max_ticks=8);

predictions = step5_predict_notes(model, npz, params);
converted = step5_convert_sliders(predictions, params);


# In[115]:


step5_save_predictions(converted);


# ## osumapper #6: Map flow generator
# 
# Generate the final map using a Generative Adversarial Network.
# 
# Parameters:
# 
# - note_distance_basis: the baseline for distance snap between notes
# - max_ticks_for_ds: max number of time ticks (each 1/4) that it uses the distance snap
# - next_from_slider_end: use slider end instead of slider head for calculating distance
# - box_loss_border, box_loss_value: it's like a barrier on the map edges that bounces off the circles
# - divisor, note_group_size: don't change unless you're using a special model built for it
# - good_epoch, max_epoch: controls the training time. less time makes it faster but risks less quality
# - g_\*, c_\*: hyperparameters used by GAN. No one knows how they work but they mysterically affect the result

# In[116]:


from act_gan import *;

gan_params = {
    "divisor" : 4,
    "good_epoch" : 12,
    "max_epoch" : 30,
    "note_group_size" : 10,
    "g_epochs" : 1,
    "c_epochs" : 1,
    "g_batch" : 25, #50
    "g_input_size" : 100, #50
    "c_true_batch" : 120, # 140
    "c_false_batch" : 5, # 5
    "c_randfalse_batch" : 5,
    "note_distance_basis" : 350,
    "next_from_slider_end" : False,
    "max_ticks_for_ds" : 16, # 8 oder 4
    "box_loss_border" : 0.1,
    "box_loss_value" : 0.4,
    "box_loss_weight" : 1
};

step6_set_gan_params(gan_params);
osu_a, data = step6_run_all();


# ### Since the generation will take a while...
# 
# we can appreciate a nice picture of Cute Sophie!!
# 
# <img src="https://i.imgur.com/Ko2wogO.jpg" />

# Do a little modding to the map.
# 
# Parameters:
# 
# - stream_regularizer: fix bad streams. integer for modes (0,1,2,3,4) 0=inactive
# - slider_mirror: mirror slider ends if they go outside map area. (0,1) 0=inactive 1=active

# In[117]:


from act_modding import *

modding_params = {
    "stream_regularizer" : 1,
    "slider_mirror" : 1
}

osu_a, data = step7_modding(osu_a, data, modding_params);


# Finally, save the data into an .osu file!

# In[118]:


from act_final import *

saved_osu_name = step8_save_osu_file(osu_a, data);

# for taiko mode only (comment out the above line and use below)
# from act_taiko_hitsounds import *
# taiko_hitsounds_params = step8_taiko_hitsounds_set_params(divisor=4, metronome_count=4)
# hitsounds = step8_apply_taiko_hitsounds(osu_a, data, params=taiko_hitsounds_params)
# saved_osu_name = step8_save_osu_file(osu_a, data, hitsounds=hitsounds);

# clean up the folder
step8_clean_up();




