from pathlib import Path

from metakernel import Magic


class DBMagic(Magic):

    def line_db(self, path='.'):
        """
        %db PATH - set Godel database

        This line magic is used to set the directory to the godel database
        to query.

        Example:
            %db /path/to/db
        """
        try:
            retval = str(Path(path).expanduser().absolute())
            self.kernel.set_variable("sparrow_database_path", retval)
        except Exception as e:
            self.kernel.Error(str(e))
            retval = None
        if retval:
            self.kernel.Print(retval)


def register_magics(kernel):
    kernel.register_magics(DBMagic)
