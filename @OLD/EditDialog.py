# Frame to edit issues.

from javax.swing import (JPanel, JLabel, JTextField, JTabbedPane, JPanel,
                         JTextField, JButton, JSplitPane, BorderFactory,
                         GroupLayout, JTextArea, JComboBox, LayoutStyle,
                         JDialog, WindowConstants)

from java.awt.event import ComponentListener
from Issue import Issue

class DialogListener(ComponentListener):
    """ComponentListener for the EditDialog."""

    def __init__(self, dialog):
        """DialogListener constructor to save a reference to the dialog."""
        self.dialog = dialog

    def componentHidden(self, event):
        """Invoked when the dialog is hidden."""
        issue = self.dialog.issue

        if self.dialog.mode == "edit":
            # edit the issue
            index = issue.index
            delattr(issue, 'index') 
            self.dialog.dlgParent.editIssue(index, issue)
        else:
            # new issue
            self.dialog.dlgParent.gotNewIssue(issue)

    def componentMoved(self, event):
        pass

    def componentResized(self, event):
        pass

    def componentShown(self, event):
        pass


class EditDialog(JDialog):
    """Represents the dialog used to edit issues or add new ones."""

    defaultIssue = Issue(
        name="Issue Type/Name",
        severity="Critical",
        host="Issue Host",
        path="Issue Path",
        description="Description",
        remediation="",
        request="",
        response=""
    )

    def loadPanel(self, issue):
        # type: (Issue) -> ()
        """Populates the panel with issue."""
        if issue is None:
            return
        
        # check if the input is the correct object
        assert isinstance(issue, Issue)

        # set textfields and textareas
        self.textName.text = issue.name
        self.textName.selectionStart = 0
        self.textHost.text = issue.host
        self.textHost.selectionStart = 0
        self.textPath.text = issue.path
        self.textPath.selectionStart = 0
        self.textAreaDescription.text = issue.description
        self.textAreaDescription.selectionStart = 0
        self.textAreaRemediation.text = issue.remediation
        self.textAreaRemediation.selectionStart = 0
        # severity combobox
        # this is case-sensitive apparently
        self.comboSeverity.setSelectedItem(issue.severity)
        # request and response tabs
        self.panelRequest.setMessage(issue.getRequest(), True)
        self.panelResponse.setMessage(issue.getResponse(), False)

    def cancelButtonAction(self, event):
        """Close the dialog when the cancel button is clicked."""
        self.dispose()

    def resetButtonAction(self, event):
        """Reset the dialog."""
        self.loadPanel(self.defaultIssue)

    def saveButtonAction(self, event):
        """Save the current issue."""
        ist = Issue(name=self.textName.text, host=self.textHost.text,
                    path=self.textPath.text,
                    description=self.textAreaDescription.text,
                    remediation=self.textAreaRemediation.text,
                    severity=str(self.comboSeverity.getSelectedItem()),
                    request=self.panelRequest.getMessage(),
                    response=self.panelResponse.getMessage())
        self.issue = ist
        if self.mode == "edit":
            # if it's in edit mode, pass the index
            self.issue.index = self.index
        self.setVisible(False)
    
    def __init__(self, callbacks, title="", modality="",
                 issue=defaultIssue):
        """Constructor to populate the dialog with the new issue."""
        self.setTitle(title)

        # holds the issue to be saved
        self.issue = issue
        # default mode is new
        self.mode = "new"

        if modality is not "":
            from java.awt.Dialog import ModalityType
            modality = modality.lower()
            # application blocks us from clicking anything else in Burp
            if modality == "application":
                self.setModalityType(ModalityType.APPLICATION_MODAL)
            if modality == "document":
                self.setModalityType(ModalityType.DOCUMENT_MODAL)
            if modality == "modeless":
                self.setModalityType(ModalityType.DOCUMENT_MODAL)
            if modality == "toolkit":
                self.setModalityType(ModalityType.DOCUMENT_MODAL)

        # assert isinstance(callbacks, IBurpExtenderCallbacks)
        # starting converted code from NetBeans
        self.labelPath = JLabel("Path")
        self.labelSeverity = JLabel("Severity")
        self.tabIssue = JTabbedPane()
        self.textAreaDescription = JTextArea()
        self.textAreaRemediation = JTextArea()
        self.panelRequest = callbacks.createMessageEditor(None, True)
        self.panelResponse = callbacks.createMessageEditor(None, True)
        # selectionStart=0 selects the text in the textfield when it is in focus
        self.textName = JTextField()
        self.textHost = JTextField()
        self.textPath = JTextField()
        self.labelHost = JLabel("Host")
        self.labelName = JLabel("Issue Type/Name")

        # buttons
        self.buttonSave = JButton("Save",
                                  actionPerformed=self.saveButtonAction)
        self.buttonCancel = JButton("Cancel",
                                    actionPerformed=self.cancelButtonAction)
        self.buttonReset = JButton("Reset",
                                   actionPerformed=self.resetButtonAction)

        # description textarea
        from java.awt import Dimension
        self.textAreaDescription.setPreferredSize(Dimension(400,500))
        self.tabIssue.addTab("Description", self.textAreaDescription)
        self.tabIssue.addTab("Remediation", self.textAreaRemediation)

        # request and response tabs
        # request tab
        self.panelRequest.setMessage("", True)
        self.tabIssue.addTab("Request", self.panelRequest.getComponent())
        # response tab
        self.panelResponse.setMessage("", False)
        self.tabIssue.addTab("Response", self.panelResponse.getComponent())

        # TODO: Populate this from outside using a config file?
        # or perhaps the extension config
        self.comboSeverity = JComboBox(["Critical", "High", "Medium", "Low",
        "Info"])
        self.comboSeverity.setSelectedIndex(-1)

        # add componentlistener
        dlgListener = DialogListener(self)
        self.addComponentListener(dlgListener)

        if issue is None:
            issue = self.defaultIssue
        
        # load the issue into the edit dialog.
        self.loadPanel(issue)

        # add the issue in the parameter to the field
        # we are doing some of the work twice but it's ok.
        if issue is not None and issue is not self.defaultIssue:
            # make sure it's the correct object
            assert isinstance(issue, Issue)
            self.mode = "edit"
            self.index = issue.index
            self.loadPanel(issue)

        # "here be dragons" GUI code
        layout = GroupLayout(self.getContentPane())
        self.getContentPane().setLayout(layout)
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.CENTER)
                .addGroup(layout.createSequentialGroup()
                          .addGroup(layout.createParallelGroup(GroupLayout.Alignment.CENTER)
                                    .addGroup(layout.createSequentialGroup()
                                              .addContainerGap()
                                              .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                                                        .addGroup(layout.createSequentialGroup()
                                                                  .addGroup(layout.createParallelGroup(GroupLayout.Alignment.TRAILING)
                                                                            .addComponent(self.labelHost)
                                                                            .addComponent(self.labelName))
                                                                  .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                                                                  .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                                                                            .addGroup(layout.createSequentialGroup()
                                                                                      .addComponent(self.textHost, GroupLayout.PREFERRED_SIZE, 212, GroupLayout.PREFERRED_SIZE)
                                                                                      .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                                                                                      .addComponent(self.labelPath)
                                                                                      .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                                                                                      .addComponent(self.textPath))
                                                                            .addGroup(GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                                                                                      .addComponent(self.textName, GroupLayout.PREFERRED_SIZE, 620, GroupLayout.PREFERRED_SIZE)
                                                                                      .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                                                                                      .addComponent(self.labelSeverity)
                                                                                      .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                                                                                      .addComponent(self.comboSeverity, GroupLayout.PREFERRED_SIZE, 182, GroupLayout.PREFERRED_SIZE))))
                                                        .addComponent(self.tabIssue)))
                                    .addGroup(layout.createSequentialGroup()
                                              .addComponent(self.buttonSave, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE)
                                              .addComponent(self.buttonReset, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE)
                                              .addComponent(self.buttonCancel, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE))
                                    )
                          .addContainerGap())
        )

        # link size of buttons together
        from javax.swing import SwingConstants
        layout.linkSize(SwingConstants.HORIZONTAL, [self.buttonCancel, self.buttonSave, self.buttonReset])

        layout.setVerticalGroup(
            layout.createParallelGroup()
                .addGroup(GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                          .addContainerGap()
                          .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                    .addComponent(self.labelName)
                                    .addComponent(self.textName, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                                    .addComponent(self.labelSeverity)
                                    .addComponent(self.comboSeverity, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                          .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                          .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                    .addComponent(self.textHost, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                                    .addComponent(self.labelPath)
                                    .addComponent(self.textPath, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                                    .addComponent(self.labelHost))
                          .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                          .addComponent(self.tabIssue)
                          .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                          .addGroup(layout.createParallelGroup()
                                    .addComponent(self.buttonSave)
                                    .addComponent(self.buttonReset)
                                    .addComponent(self.buttonCancel))
                          .addContainerGap())
        )
        # end of converted code from NetBeans

    def display(self, parent):
        """packs and shows the frame."""
        self.pack()
        # setlocation must be AFTER pack
        # source: https://stackoverflow.com/a/22615038
        self.dlgParent = parent
        self.setLocationRelativeTo(self.dlgParent.panel)
        # self.show()
        self.setVisible(True)

    def getIssue(self):
        """Returns the dialog issue."""
        return self.issue