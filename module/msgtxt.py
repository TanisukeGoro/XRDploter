""" define the font color in terminal """
import shutil

class MsgTxt:
    def __init__(
        self,
        PLTMODE="(online | offline)",
        SHARING="(private | public)",
        SAVE_DIR="(Save direcry)",
        FILEOPT="(new | overwrite | extend | append)"):

        terminal_size = shutil.get_terminal_size()
        colum = terminal_size.columns
        if colum > 100:
            colum = 100
            

        self._plotmode = PLTMODE
        self._sharing  = SHARING
        self._save_dir = SAVE_DIR
        self._fileopt  = FILEOPT
        self._colum    = colum


    def get_space_sub_routine(self, char):
        rm = self._colum - len(char) - 4
        space1 = int(rm/2)
        space2 =int(rm - space1)
        return (space1, space2)


    def __str__(self):
        wl = 'Welcome to the XRD graphing program !!'
        wl_space1, wl_space2 = self.get_space_sub_routine(wl)
        vr='ver 1.0.0  2018.11.11'
        vr_space1, vr_space2 = self.get_space_sub_routine(vr)
        nc ='now configuration'
        nc_space1, nc_space2 = self.get_space_sub_routine(nc)

        welcome_XRDploter = '\n {0} \n'.format('+'*(self._colum-2)) + \
          ' +{0}{1}{2} + \n'.format(' ' * wl_space1, wl, ' ' * wl_space2) + \
          ' +{0}{1}{2}+ \n'.format(' ' * vr_space1, vr, ' ' * vr_space2) + \
          ' +{0}{1}{2}+ \n'.format(' ' * nc_space1, nc, ' ' * nc_space2) + \
          ' +  Plot mode   : {0}{1}+ \n'.format(self._plotmode, ' '*(self._colum-20-len(self._plotmode))) + \
          ' +  Sharing     : {0}{1}+ \n'.format(self._sharing, ' '*(self._colum-20-len(self._sharing))) + \
          ' +  Save dir    : {0}{1}+ \n'.format(self._save_dir, ' '*(self._colum-20-len(self._save_dir))) + \
          ' +  File update : {0}{1}+ \n'.format(self._fileopt, ' '*(self._colum-20-len(self._fileopt))) + \
          ' {0} '.format('+'*(self._colum-2))

        return welcome_XRDploter

    def msgbox(self):
        gt= 'Input Graph title'
        gt_space1, gt_space2 = self.get_space_sub_routine(gt)
        fn= 'Input File name'
        fn_space1, fn_space2 = self.get_space_sub_routine(fn)
        mp= 'Lets Multiple plot.'
        mp_space1, mp_space2 = self.get_space_sub_routine(mp)
        wm= 'How mach do you shift to the y-axis?'
        wm_space1, wm_space2 = self.get_space_sub_routine(wm)
        er=  'Error !!'
        er_space1, er_space2 = self.get_space_sub_routine(er)
        xy=  'The both number of x and y element  do not match.'
        xy_space1, xy_space2 = self.get_space_sub_routine(xy)

        self.input_graphtitle = '\n {0} \n'.format('+'*(self._colum-2)) + \
                              ' +{0}{1}{2}+ \n'.format(' ' * gt_space1, gt, ' ' * gt_space2) + \
                              ' {0} \n'.format('+'*(self._colum-2))
        # print (input_graphtitle)

        self.input_filename   = '\n {0} \n'.format('+'*(self._colum-2)) + \
                              ' +{0}{1}{2}+ \n'.format(' ' * fn_space1, fn, ' ' * fn_space2) + \
                              ' {0} \n'.format('+'*(self._colum-2))
        # print (input_filename)

        self.multiplot_flag   = '\n {0} \n'.format('+'*(self._colum-2)) + \
                              ' +{0}{1}{2}+ \n'.format(' ' * mp_space1, mp, ' ' * mp_space2) + \
                              ' +{0}{1}{2}+\n'.format(' ' * wm_space1, wm, ' ' * wm_space2) + \
                              ' {0} \n'.format('+'*(self._colum-2))
        # print (multiplot_flag)

        self.error_xy_trace   = '\n {0} \n'.format('+'*(self._colum-2)) + \
                              ' +{0}{1}{2}+ \n'.format(' ' * er_space1, er, ' ' * er_space2) + \
                              ' +{0}{1}{2}+\n'.format(' ' * xy_space1, xy, ' ' * xy_space2) + \
                              ' {0} \n'.format('+'*(self._colum-2))
        # print (error_xy_trace)


    def plot_file_name(self, argc):
        Ca = 'Caution !!'
        Ca_space1, Ca_space2 = self.get_space_sub_routine(Ca)
        tl = 'File name character length is too long.'
        tl_space1, tl_space2 = self.get_space_sub_routine(tl)
        sp = ''
        sp_space1, sp_space2 = self.get_space_sub_routine(sp)
        fi = '↓ File names ↓'
        fi_space1, fi_space2 = self.get_space_sub_routine(fi)
        dy = 'Do you change this file name? yse(y) / no(n)'
        dy_space1, dy_space2 = self.get_space_sub_routine(dy)

        self._fn = argc
        self.caution_charleng  = '\n {0} \n'.format('+'*(self._colum-2)) + \
                                  ' +{0}{1}{2}+ \n'.format(' ' * Ca_space1, Ca, ' ' * Ca_space2) + \
                                  ' +{0}{1}{2}+ \n'.format(' ' * tl_space1, tl, ' ' * tl_space2) + \
                                  ' +{0}{1}{2}+ \n'.format(' ' * sp_space1, sp, ' ' * sp_space2) + \
                                  ' +{0}{1}{2}+ \n'.format(' ' * fi_space1, fi, ' ' * fi_space2)+ \
                                  ' + >> {0}{1}+ \n'.format(self._fn, ' '*(self._colum-8-len(self._fn))) + \
                                  ' +{0}{1}{2}+ \n'.format(' ' * sp_space1, sp, ' ' * sp_space2) + \
                                  ' +{0}{1}{2}+ \n'.format(' ' * dy_space1, dy, ' ' * dy_space2) + \
                                  ' {0} \n'.format('+'*(self._colum-2))
        print (self.caution_charleng)
