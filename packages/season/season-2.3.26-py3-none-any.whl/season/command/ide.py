import season
import os
from argh import arg

@arg('action', default=None, help="install | remove | upgrade | build")
def ide(action, *args):
    PATH_FRAMEWORK = os.path.dirname(os.path.dirname(__file__))
    frameworkfs = season.util.os.FileSystem(PATH_FRAMEWORK)
    fs = season.util.os.FileSystem(os.getcwd())
    idefs = season.util.os.FileSystem(os.path.join(os.getcwd(), "ide"))
    pluginfs = season.util.os.FileSystem(os.path.join(os.getcwd(), "plugin"))
    cachefs = season.util.os.FileSystem(os.path.join(os.getcwd(), ".wiz.cache"))

    if fs.exists(os.path.join("public", "app.py")) == False:
        print("Invalid Project path: wiz structure not found in this folder.")
        return

    app = season.app(path=os.getcwd())
    workspace = app.wiz().workspace("ide")

    class Command:
        def install(self):
            if idefs.exists():
                print("WIZ IDE Already Installed")
                return False

            print("installing WIZ IDE...")
            fs.copy(frameworkfs.abspath(os.path.join("data", "ide")), "ide")
            
            if pluginfs.exists() == False:
                fs.copy(frameworkfs.abspath(os.path.join("data", "plugin")), "plugin")

            workspace.build.clean()
            workspace.build()
            print("WIZ IDE installed")
            return True

        def remove(self):
            if idefs.exists() == False:
                print("WIZ IDE is not installed")
                return False
            idefs.remove()
            print("WIZ IDE removed")
            return True

        def upgrade(self, *args):
            mode = 'all'
            if len(args) > 1:
                mode = args[0]
            
            if mode in ['all', 'core']:
                print("Upgrading WIZ IDE...")
                idefs.remove()
                fs.copy(frameworkfs.abspath(os.path.join("data", "ide")), "ide")
                workspace.build.clean()
                workspace.build()

            if mode in ['all', 'plugin']:
                print("Upgrading WIZ IDE Plugins...")
                plugin = season.plugin(os.getcwd())
                plugin.uninstall("portal")
                plugin.upgrade("core")
                plugin.upgrade("workspace")
                plugin.upgrade("git")
                plugin.upgrade("utility")
                workspace.build()

            print("WIZ IDE upgraded")

        def build(self):
            if idefs.exists() == False:
                print("WIZ IDE is not installed")
                return False
            workspace.build()
            
        def __call__(self, name, args):
            cachefs.delete()
            cachefs.makedirs()
            fn = getattr(self, name)
            fn(*args)
            cachefs.delete()

    cmd = Command()
    cmd(action, args)
    