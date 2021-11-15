from nextcord.ext import commands
from modules.osumapper.act_timing import *
from modules.osumapper.act_rhythm_calc import *
from modules.osumapper.act_gan import *
from modules.osumapper.act_modding import *
from modules.osumapper.act_final import *


music_path = r"audio.mp3"


class generate_beatmap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Generates a osu!beatmap based on a send audio file")
    async def make_map(self, ctx):

        file_path = get_timed_osu_file(music_path, game_mode=0);
        await ctx.send (f"getting BPM and timings from the provided audio file ... please wait🦊")
        
        # Ignore that this(V) it is getting displayed as an error.
        step4_read_new_map(file_path);
        model = step5_load_model();
        npz = step5_load_npz();
        params = step5_set_params(dist_multiplier=1, note_density=0.75, slider_favor=0.1, divisor_favor=[0] * 4, slider_max_ticks=8);

        predictions = step5_predict_notes(model, npz, params);
        converted = step5_convert_sliders(predictions, params);
        step5_save_predictions(converted);

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


        modding_params = {
            "stream_regularizer" : 1,
            "slider_mirror" : 1
        }

        osu_a, data = step7_modding(osu_a, data, modding_params);

        saved_osu_name = step8_save_osu_file(osu_a, data);

        # clean up
        step8_clean_up();


def setup(bot):
    bot.add_cog(generate_beatmap(bot))