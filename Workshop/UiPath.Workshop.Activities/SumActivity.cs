using System.Activities;
using System.ComponentModel;

namespace UiPath.Workshop.Activities
{
    public class SumActivity : CodeActivity
    {
        [RequiredArgument]
        [Category("Input")]
        [DisplayName("First number")]
        [Description("The first operand of the sum.")]
        public InArgument<int> FirstNumber { get; set; }

        [Category("Input")]
        [DisplayName("Second number")]
        [Description("The second operand of the sum.")]
        public InArgument<int> SecondNumber { get; set; }

        [Category("Output")]
        [DisplayName("Result")]
        [Description("The result.")]
        public OutArgument<int> SumResult { get; set; }
            
        protected override void Execute(CodeActivityContext context)
        {
            int first = FirstNumber.Get(context);
            int second = SecondNumber.Get(context);

            SumResult.Set(context, first + second);
        }
    }
}
