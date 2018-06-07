using System.Activities.Presentation.Metadata;
using System.ComponentModel;

namespace UiPath.Workshop.Activities.Design
{
    public class DesignerMetadata : IRegisterMetadata
    {
        public void Register()
        {
            AttributeTableBuilder builder = new AttributeTableBuilder();

            builder.AddCustomAttributes(typeof(SumActivity), new DesignerAttribute(typeof(SumActivityDesigner)));

            MetadataStore.AddAttributeTable(builder.CreateTable());
        }
    }
}
