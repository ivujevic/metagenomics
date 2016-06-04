import controllers.TaxTree;
import play.*;
import play.Application;

import javax.inject.Inject;
import javax.swing.text.PlainDocument;

/**
 * Created by vujevic on 04.06.16..
 */
public class Global extends GlobalSettings{

    @Override
    public void onStart(Application app) {
        String namesPath = Play.application().configuration().getString("tax.names");

        //System.out.println("====================================================== " + a);
        TaxTree.readInMemory(namesPath);
    }
}
