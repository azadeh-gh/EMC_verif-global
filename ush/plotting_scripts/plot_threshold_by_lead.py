from __future__ import (print_function, division)
import os
import numpy as np
import plot_util as plot_util
import pandas as pd
import warnings
import logging
import datetime
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.gridspec as gridspec

warnings.filterwarnings('ignore')
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelsize'] = 15
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 15
plt.rcParams['ytick.labelsize'] = 15
plt.rcParams['axes.titlesize'] = 15
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.formatter.useoffset'] = False
###import cmocean
###cmap_bias = cmocean.cm.curl
###cmap = cmocean.cm.tempo
###cmap_diff = cmocean.cm.balance
cmap_bias = plt.cm.PiYG_r
cmap = plt.cm.BuPu
cmap_diff = plt.cm.coolwarm_r

verif_case = os.environ['VERIF_CASE']
verif_type = os.environ['VERIF_TYPE']
plot_time = os.environ['PLOT_TIME']
start_date_YYYYmmdd = os.environ['START_DATE_YYYYmmdd']
end_date_YYYYmmdd = os.environ['END_DATE_YYYYmmdd']
start_date_YYYYmmdd_dt = datetime.datetime.strptime(os.environ['START_DATE_YYYYmmdd'], "%Y%m%d")
end_date_YYYYmmdd_dt = datetime.datetime.strptime(os.environ['END_DATE_YYYYmmdd'], "%Y%m%d")
valid_time_info = os.environ['VALID_TIME_INFO'].replace('"','').split(", ")
init_time_info = os.environ['INIT_TIME_INFO'].replace('"','').split(", ")
fcst_var_name = os.environ['FCST_VAR_NAME']
fcst_var_name = os.environ['FCST_VAR_NAME']
fcst_var_extra = (
    os.environ['FCST_VAR_EXTRA'].replace(" ", "")
    .replace("=","").replace(";","").replace('"','')
    .replace("'","").replace(",","-").replace("_","")
)
if fcst_var_extra == "None":
    fcst_var_extra = ""
if os.environ['FCST_VAR_EXTRA'] == "None":
    fcst_var_extra_title = ""
else:
    fcst_var_extra_title = " "+os.environ['FCST_VAR_EXTRA']+" "
fcst_var_level = os.environ['FCST_VAR_LEVEL']
fcst_var_thresh_list = os.environ['FCST_VAR_THRESH_LIST'].split(", ")
fcst_var_thresh_format_list = []
fcst_var_thresh_val_list = []
for thresh in fcst_var_thresh_list:
    thresh_format = (
        thresh.replace(" ","")
        .replace(">=","ge").replace("<=","le")
        .replace(">","gt").replace("<","lt")
        .replace("==","eq").replace("!=","ne")
    )
    fcst_var_thresh_format_list.append(thresh_format)
    thresh_val = (
        thresh.replace(" ","")
        .replace(">=","").replace("<=","")
        .replace(">","").replace("<","")
        .replace("==","").replace("!=","")
        .replace("ge","").replace("le","")
        .replace("gt","").replace("lt","")
        .replace("eq","").replace("ne","")
    )
    fcst_var_thresh_val_list.append(thresh_val)
fcst_var_thresh_val_array = np.asarray(fcst_var_thresh_val_list, dtype=float)
fcst_var_thresh_counts = np.arange(0, len(fcst_var_thresh_list), dtype=int)
obs_var_name = os.environ['OBS_VAR_NAME']
obs_var_extra = (
    os.environ['OBS_VAR_EXTRA'].replace(" ", "")
    .replace("=","").replace(";","")
    .replace('"','').replace("'","")
    .replace(",","-").replace("_","")
)
if obs_var_extra == "None":
    obs_var_extra = ""
if os.environ['OBS_VAR_EXTRA'] == "None":
    obs_var_extra_title = ""
else:
    obs_var_extra_title = " "+os.environ['OBS_VAR_EXTRA']+" "
obs_var_level = os.environ['OBS_VAR_LEVEL']
obs_var_thresh_list = os.environ['OBS_VAR_THRESH_LIST'].split(", ")
obs_var_thresh_format_list = []
obs_var_thresh_val_list = []
for thresh in obs_var_thresh_list:
    thresh_format = (
        thresh.replace(" ","")
        .replace(">=","ge").replace("<=","le")
        .replace(">","gt").replace("<","lt")
        .replace("==","eq").replace("!=","ne")
    )
    obs_var_thresh_format_list.append(thresh_format)
    thresh_val = (
        thresh.replace(" ","")
        .replace(">=","").replace("<=","")
        .replace(">","").replace("<","")
        .replace("==","").replace("!=","")
        .replace("ge","").replace("le","")
        .replace("gt","").replace("lt","")
        .replace("eq","").replace("ne","")
    )
    obs_var_thresh_val_list.append(thresh_val)
interp = os.environ['INTERP']
region = os.environ['REGION']
lead_list = os.environ['LEAD_LIST'].split(", ")
leads = np.asarray(lead_list).astype(float)
stat_file_input_dir_base = os.environ['STAT_FILES_INPUT_DIR']
plotting_out_dir = os.environ['PLOTTING_OUT_DIR_FULL']
plotting_out_dir_data = os.path.join(plotting_out_dir,
                                     "data",
                                     plot_time+start_date_YYYYmmdd+"to"+end_date_YYYYmmdd
                                     +"_valid"+valid_time_info[0]+"to"+valid_time_info[-1]+"Z"
                                     +"_init"+init_time_info[0]+"to"+init_time_info[-1]+"Z")
plotting_out_dir_imgs = os.path.join(plotting_out_dir,
                                     "imgs")
if not os.path.exists(plotting_out_dir_data):
    os.makedirs(plotting_out_dir_data)
if not os.path.exists(plotting_out_dir_imgs):
    os.makedirs(plotting_out_dir_imgs)
plot_stats_list = os.environ['PLOT_STATS_LIST'].split(", ")
model_name_list = os.environ['MODEL_NAME_LIST'].split(" ")
model_plot_name_list = os.environ['MODEL_PLOT_NAME_LIST'].split(" ")
model_info = zip(model_name_list, model_plot_name_list)
mean_file_cols = [ "LEADS", "VALS", "OVALS" ]
ci_file_cols = [ "LEADS", "VALS" ]
ci_method = os.environ['CI_METHOD']
grid = os.environ['VERIF_GRID']
logger = logging.getLogger(os.environ['LOGGING_FILENAME'])
logger.setLevel(os.environ['LOGGING_LEVEL'])
formatter = logging.Formatter("%(asctime)s.%(msecs)03d (%(filename)s:%(lineno)d)"
                              +"%(levelname)s: %(message)s","%m/%d %H:%M:%S")
file_handler = logging.FileHandler(os.environ['LOGGING_FILENAME'], mode='a')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
noaa_logo_img_array = matplotlib.image.imread(os.path.join(os.environ['USHverif_global'],
                                                           'plotting_scripts',
                                                           'noaa.png'))
nmodels = len(model_name_list)
fcst_var_thresh_val_array = np.asarray(fcst_var_thresh_val_list, dtype=float)
xx, yy = np.meshgrid(fcst_var_thresh_counts,leads)
for stat in plot_stats_list:
    logger.debug("Working on "+stat)
    stat_plot_name = plot_util.get_stat_plot_name(logger, 
                                                  stat)
    logger.info("Reading in model data")
    for model in model_info:
        model_num = model_info.index(model) + 1
        model_index = model_info.index(model)
        model_name = model[0]
        model_plot_name = model[1]
        model_thresh_mean_data = np.empty([len(lead_list),len(fcst_var_thresh_list)])
        model_thresh_mean_data.fill(np.nan)
        if stat == 'fbar_obar':
            obs_thresh_mean_data = np.empty([len(lead_list),len(obs_var_thresh_list)])
            obs_thresh_mean_data.fill(np.nan)
            mean_file_cols = [ "LEADS", "VALS", "OVALS" ]
        for vt in range(len(fcst_var_thresh_format_list)):
            fcst_var_thresh = fcst_var_thresh_format_list[vt]
            obs_var_thresh = obs_var_thresh_format_list[vt]
            logger.debug("Processing data for VAR_THRESH "+fcst_var_thresh)
            model_mean_file = os.path.join(plotting_out_dir_data, 
                                           model_plot_name
                                           +"_"+stat
                                           #+"_"+plot_time+start_date_YYYYmmdd+"to"+end_date_YYYYmmdd
                                           #+"_valid"+valid_time_info[0]+"to"+valid_time_info[-1]+"Z"
                                           #+"_init"+init_time_info[0]+"to"+init_time_info[-1]+"Z"
                                           +"_fcst"+fcst_var_name+fcst_var_level+fcst_var_extra+fcst_var_thresh
                                           +"_obs"+obs_var_name+obs_var_level+obs_var_extra+obs_var_thresh
                                           +"_interp"+interp
                                           +"_region"+region
                                           +"_LEAD_MEAN.txt")
            if os.path.exists(model_mean_file):
                nrow = sum(1 for line in open(model_mean_file))
                if nrow == 0: 
                    logger.warning("Model "+str(model_num)+" "
                                   +model_name+" with plot name "
                                   +model_plot_name+" file: "
                                   +model_mean_file+" empty")
                else:
                    logger.debug("Model "+str(model_num)+" "
                                 +model_name+" with plot name "
                                 +model_plot_name+" file: "
                                 +model_mean_file+" exists")
                    model_mean_file_data = pd.read_csv(model_mean_file, 
                                                       sep=" ", 
                                                       header=None, 
                                                       names=mean_file_cols, 
                                                       dtype=str)
                    model_mean_file_data_leads = model_mean_file_data.loc[:]['LEADS'].tolist()
                    model_mean_file_data_vals = model_mean_file_data.loc[:]['VALS'].tolist()
                    if stat == 'fbar_obar':
                        obs_mean_file_data_vals = model_mean_file_data.loc[:]['OVALS'].tolist()
                    for lead in lead_list:
                        lead_index = lead_list.index(lead)
                        if lead in model_mean_file_data_leads:
                            model_mean_file_data_lead_index = model_mean_file_data_leads.index(lead)
                            if model_mean_file_data_vals[model_mean_file_data_lead_index] == "--":
                                model_thresh_mean_data[lead_index,vt] = np.nan
                            else:
                                model_thresh_mean_data[lead_index,vt] = float(
                                    model_mean_file_data_vals[model_mean_file_data_lead_index]
                                )
                            if stat == 'fbar_obar':
                                if obs_mean_file_data_vals[model_mean_file_data_lead_index] == "--":
                                    obs_thresh_mean_data[lead_index,vt] = np.nan
                                else:
                                    obs_thresh_mean_data[lead_index,vt] = float(
                                        obs_mean_file_data_vals[model_mean_file_data_lead_index]
                                    )                        
            else:
                logger.warning("Model "+str(model_num)+" "
                               +model_name+" with plot name "
                               +model_plot_name+" file: "
                               +model_mean_file+" does not exist")
        if nmodels > 8:
            logger.error("Too many models selected, max. is 8")
            exit(1)
        if model_num == 1:
            if stat == 'fbar_obar':
                nsubplots = nmodels + 1
            else:
                nsubplots = nmodels
            if nsubplots == 1:
                fig = plt.figure(figsize=(10,12))
                gs = gridspec.GridSpec(1,1)
            elif nsubplots == 2:
                fig = plt.figure(figsize=(10,12))
                gs = gridspec.GridSpec(2,1)
                gs.update(hspace=0.35)
            elif nsubplots > 2 and nsubplots <= 4:
                fig = plt.figure(figsize=(20,12))
                gs = gridspec.GridSpec(2,2)
                gs.update(wspace=0.4, hspace=0.35)
            elif nsubplots > 4 and nsubplots <= 6:
                fig = plt.figure(figsize=(30,12))
                gs = gridspec.GridSpec(2,3)
                gs.update(wspace=0.4, hspace=0.35)
            elif nsubplots > 6 and nsubplots <= 9:
                fig = plt.figure(figsize=(30,18))
                gs = gridspec.GridSpec(3,3)
                gs.update(wspace=0.4, hspace=0.35)
            if stat == 'fbar_obar':
                logger.debug("Plotting observations")
                ax = plt.subplot(gs[0])
                ax.grid(True)
                ax.tick_params(axis='x', pad=15)
                ax.set_xticks(fcst_var_thresh_counts)
                ax.set_xlim([fcst_var_thresh_counts[0], fcst_var_thresh_counts[-1]])
                ax.set_xticklabels(fcst_var_thresh_list)
                ax.set_xlabel("Forecast Threshold", labelpad=20)
                ax.tick_params(axis='y', pad=15)
                ax.set_yticks(leads)
                ax.set_ylim([leads[0], leads[-1]])
                ax.set_ylabel("Forecast Lead", labelpad=20)
                ax.set_title('obs', loc='left')
                CF0 = ax.contourf(xx, yy, obs_thresh_mean_data,
                                  cmap=cmap,
                                  extend='both')
                C0 = ax.contour(xx, yy, obs_thresh_mean_data,
                                levels=CF0.levels,
                                colors='k',
                                linewidths=1.0)
                ax.clabel(C0,
                          C0.levels,
                          fmt='%1.2f',
                          inline=True,
                          fontsize=12.5)
        if stat == 'fbar_obar':
           ax = plt.subplot(gs[model_index+1])
        else:
           ax = plt.subplot(gs[model_index])
        ax.grid(True)
        ax.tick_params(axis='x', pad=15)
        ax.set_xticks(fcst_var_thresh_counts)
        ax.set_xlim([fcst_var_thresh_counts[0], fcst_var_thresh_counts[-1]])
        ax.set_xticklabels(fcst_var_thresh_list)
        ax.set_xlabel("Forecast Threshold", labelpad=20)
        ax.tick_params(axis='y', pad=15)
        ax.set_yticks(leads)
        ax.set_ylim([leads[0], leads[-1]])
        ax.set_ylabel("Forecast Lead", labelpad=20)
        if stat == "fbar_obar":
            logger.debug("Plotting model "+str(model_num)
                         +" "+model_name+" - obs"
                         +" with name on plot "+model_plot_name
                         +" - obs")
            ax.set_title(model_plot_name+" - obs", loc='left')
            model_obs_diff = model_thresh_mean_data - obs_thresh_mean_data
            if model_num == 1:
                clevels_diff = plot_util.get_clevels(model_obs_diff)
                CF1 = ax.contourf(xx, yy, model_obs_diff,
                                  levels=clevels_diff,
                                  cmap=cmap_diff,
                                  locator=matplotlib.ticker.MaxNLocator(symmetric=True),
                                  extend='both')
                C1 = ax.contour(xx, yy, model_obs_diff,
                                levels=CF1.levels,
                                colors='k',
                                linewidths=1.0)
                ax.clabel(C1,
                          C1.levels,
                          fmt='%1.2f',
                          inline=True,
                          fontsize=12.5)
            else:
                CF = ax.contourf(xx, yy, model_obs_diff,
                                 levels=CF1.levels,
                                 cmap=cmap_diff,
                                 locator=matplotlib.ticker.MaxNLocator(symmetric=True),
                                 extend='both')
                C = ax.contour(xx, yy, model_obs_diff,
                               levels=CF1.levels,
                               colors='k',
                               linewidths=1.0)
                ax.clabel(C,
                          C.levels,
                          fmt='%1.2f',
                          inline=True,
                          fontsize=12.5)
        elif stat == "bias":
            logger.debug("Plotting model "+str(model_num)+" "
                         +model_name+" with name on plot "
                         +model_plot_name)
            ax.set_title(model_plot_name, loc='left')
            if model_num == 1:
                clevels_bias = plot_util.get_clevels(model_thresh_mean_data)
                CF1 = ax.contourf(xx, yy, model_thresh_mean_data,
                                  levels=clevels_bias,
                                  cmap=cmap_bias,
                                  locator=matplotlib.ticker.MaxNLocator(symmetric=True),
                                  extend='both')
                C1 = ax.contour(xx, yy, model_thresh_mean_data,
                                levels=CF1.levels,
                                colors='k',
                                linewidths=1.0)
                ax.clabel(C1,
                          C1.levels,
                          fmt='%1.2f',
                          inline=True,
                          fontsize=12.5)
            else:
                CF = ax.contourf(xx, yy, model_thresh_mean_data,
                                 levels=CF1.levels,
                                 cmap=cmap_bias,
                                 extend='both')
                C = ax.contour(xx, yy, model_thresh_mean_data,
                               levels=CF1.levels,
                               colors='k',
                               linewidths=1.0)
                ax.clabel(C,
                          C.levels,
                          fmt='%1.2f',
                          inline=True,
                          fontsize=12.5)
        else:
            if model_num == 1:
                logger.debug("Plotting model "+str(model_num)+" "
                             +model_name+" with name on plot "
                             +model_plot_name)
                model1_name = model_name
                model1_plot_name = model_plot_name
                model1_thresh_mean_data = model_thresh_mean_data
                ax.set_title(model_plot_name, loc='left')
                CF1 = ax.contourf(xx, yy, model_thresh_mean_data,
                                  cmap=cmap,
                                  extend='both')
                C1 = ax.contour(xx, yy, model_thresh_mean_data,
                                levels=CF1.levels,
                                colors='k',
                                linewidths=1.0)
                ax.clabel(C1,
                          C1.levels,
                          fmt='%1.2f',
                          inline=True,
                          fontsize=12.5)
            else:
                logger.debug("Plotting model "+str(model_num)+" "
                             +model_name+" - model 1 "+model1_name+" with name on plot "
                             +model_plot_name+"-"+model1_plot_name)
                ax.set_title(model_plot_name+"-"+model1_plot_name, loc='left')
                model_model1_diff = model_thresh_mean_data - model1_thresh_mean_data
                if model_num == 2:
                    clevels_diff = plot_util.get_clevels(model_model1_diff)
                    CF2 = ax.contourf(xx, yy, model_model1_diff,
                                      levels=clevels_diff,
                                      cmap=cmap_diff,
                                      locator=matplotlib.ticker.MaxNLocator(symmetric=True),
                                      extend='both')
                    C2 = ax.contour(xx, yy, model_model1_diff,
                                    levels=CF2.levels,
                                    colors='k',
                                    linewidths=1.0)
                    ax.clabel(C2,
                              C2.levels,
                              fmt='%1.2f',
                              inline=True,
                              fontsize=12.5)
                else:
                    CF = ax.contourf(xx, yy, model_model1_diff,
                                     levels=CF2.levels,
                                     cmap=cmap_diff,
                                     locator=matplotlib.ticker.MaxNLocator(symmetric=True),
                                     extend='both')
                    C = ax.contour(xx, yy, model_model1_diff,
                                   levels=CF2.levels,
                                   colors='k',
                                   linewidths=1.0)
                    ax.clabel(C,
                              C.levels,
                              fmt='%1.2f',
                              inline=True,
                              fontsize=12.5)
    cax = fig.add_axes([0.1, -0.05, 0.8, 0.05])
    if stat == "fbar_obar":
        cbar = fig.colorbar(CF1,
                            cax=cax,
                            orientation='horizontal',
                            ticks=CF1.levels)
    elif stat == "bias":
        cbar = fig.colorbar(CF1,
                            cax=cax,
                            orientation='horizontal',
                            ticks=CF1.levels)
    else:
        if nsubplots == 1:
            cbar = fig.colorbar(CF1,
                                cax=cax,
                                orientation='horizontal',
                                ticks=CF1.levels)
        else:
            cbar = fig.colorbar(CF2,
                                cax=cax,
                                orientation='horizontal',
                                ticks=CF2.levels)
    if grid == region:
        gridregion = grid
        gridregion_title = grid
    else:
        gridregion = grid+region
        gridregion_title = grid+"-"+region
    if interp[0:2] == 'WV':
        fcst_var_name = fcst_var_name+"_"+interp
    if plot_time == 'valid':
        if verif_case == 'precip':
            savefig_name = os.path.join(plotting_out_dir_imgs,
                                        stat
                                        +"_valid"+valid_time_info[0][0:2]+"Z"
                                        +"_"+fcst_var_name+"_"+fcst_var_level+"_all"
                                        +"_fhrmean"
                                        +"_"+gridregion
                                        +".png")
            full_title = (
                stat_plot_name+"\n"
                +fcst_var_name+" "+fcst_var_level+fcst_var_extra_title+" threshold mean"
                +" "+gridregion_title+"\n"
                +plot_time+": "
                +start_date_YYYYmmdd_dt.strftime('%d%b%Y')+"-"
                +end_date_YYYYmmdd_dt.strftime('%d%b%Y')
                +" "+valid_time_info[0][0:2]+"Z"
                +", forecast mean"
            )
    elif plot_time == 'init':
        if verif_case == 'precip':
            savefig_name = os.path.join(plotting_out_dir_imgs,
                                        stat
                                        +"_init"+init_time_info[0][0:2]+"Z"
                                        +"_"+fcst_var_name+"_"+fcst_var_level+"_all"
                                        +"_fhrmean"
                                        +"_"+gridregion
                                        +".png")
            full_title = (
                stat_plot_name+"\n"
                +fcst_var_name+" "+fcst_var_level+fcst_var_extra_title+" threshold mean"
                +" "+gridregion_title+"\n"
                +plot_time+": "
                +start_date_YYYYmmdd_dt.strftime('%d%b%Y')+"-"
                +end_date_YYYYmmdd_dt.strftime('%d%b%Y')
                +" "+init_time_info[0][0:2]+"Z"
                +", forecast hour mean"
            )
    fig.suptitle(full_title, fontsize=14, fontweight='bold')
    fig.figimage(noaa_logo_img_array, 1, 1, zorder=1, alpha=0.5)
    logger.info("Saving image as "+savefig_name)
    plt.savefig(savefig_name, bbox_inches='tight')
    plt.close()
