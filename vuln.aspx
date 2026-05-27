<%@ Page Language="C#" AutoEventWireup="true" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title>ViewState Lab</title>
</head>
<body>
    <form id="form1" runat="server">
        <h2>ViewState Test Page</h2>
        <asp:TextBox ID="txtInput" runat="server" placeholder="Type something..." />
        <asp:Button ID="btnSubmit" runat="server" Text="Submit" OnClick="btnSubmit_Click" />
        <br /><br />
        <asp:Label ID="lblResult" runat="server" ForeColor="Green" />
    </form>
</body>
</html>
<script runat="server">
    protected void btnSubmit_Click(object sender, EventArgs e) {
        lblResult.Text = "You entered: " + Server.HtmlEncode(txtInput.Text);
    }
</script>
