using System.Activities.Presentation.Metadata;
using System.ComponentModel;

namespace UiPath.Workshop.Activities.Design
{
    public class DesignerMetadata : IRegisterMetadata
    {
        public void Register()
        {
            AttributeTableBuilder tableBuilder = new AttributeTableBuilder();

            tableBuilder.AddCustomAttributes(typeof(HelloWorldActivity), new DesignerAttribute(typeof(HelloWorldActivityDesigner)));
            tableBuilder.AddCustomAttributes(typeof(DemoScopeActivity), new DesignerAttribute(typeof(DemoScopeActivityDesigner)));

            MetadataStore.AddAttributeTable(tableBuilder.CreateTable());
        }
    }
}
