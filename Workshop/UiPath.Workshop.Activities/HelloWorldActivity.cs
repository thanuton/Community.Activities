using System;
using System.Activities;
using System.Activities.Validation;
using System.ComponentModel;

namespace UiPath.Workshop.Activities
{
    [Category("Workshop")]
    [DisplayName("Demo Hello World")]
    [Description("Receives a name as input and outputs a greeting.")]
    public class HelloWorldActivity : CodeActivity
    {
        [RequiredArgument]
        [Category("Input")]
        [DisplayName("Your name")]
        [Description("Name of the person to be greeted.")]
        public InArgument<string> Name { get; set; }

        public int SomeNumber { get; set; }

        [Category("Output")]
        [DisplayName("Greeting")]
        [Description("The outputed greeting.")]
        public OutArgument<string> Result { get; set; }

        protected override void CacheMetadata(CodeActivityMetadata metadata)
        {
            base.CacheMetadata(metadata);

            if (SomeNumber < 0)
            {
                ValidationError error = new ValidationError("SomeNumber cannot be negative.", true, nameof(SomeNumber));
                metadata.AddValidationError(error);
            }
        }

        protected override void Execute(CodeActivityContext context)
        {
            string name = Name.Get(context);

            if (string.IsNullOrWhiteSpace(name))
            {
                PropertyDescriptor nameFromParentProperty = context.DataContext.GetProperties()["NameFromParent"];
                string nameFromParent = nameFromParentProperty?.GetValue(context.DataContext) as string;

                if (string.IsNullOrWhiteSpace(nameFromParent))
                {
                    throw new ArgumentNullException(nameof(Name));
                }
                else
                {
                    name = nameFromParent;
                }
            }

            Result.Set(context, "Hello, " + name + "!");
        }
    }
}
