import os

from govlabstatic.cli import Manager

manager = Manager(
    site_name='example site',
    site={
        'outpath': 'site',

    },
    sass_src_path=os.path.join('sass', 'styles.scss'),
    sass_dest_path=os.path.join('site', 'static', 'styles', 'styles.css')
)

if __name__ == '__main__':
    manager.run()
