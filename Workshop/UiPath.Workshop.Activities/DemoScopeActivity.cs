using System;
using System.Activities;
using System.Activities.Statements;
using System.Collections.Generic;
using System.ComponentModel;

namespace UiPath.Workshop.Activities
{
    public class DemoScopeActivity : NativeActivity
    {
        [Browsable(false)]
        public ActivityAction<string> Body { get; set; }

        public DemoScopeActivity()
        {
            Sequence sequence = new Sequence();
            sequence.DisplayName = "Do";

            Body = new ActivityAction<string>();
            Body.Argument = new DelegateInArgument<string>("NameFromParent");
            Body.Handler = sequence;
        }

        protected override void CacheMetadata(NativeActivityMetadata metadata)
        {
            base.CacheMetadata(metadata);
        }

        protected override void Execute(NativeActivityContext context)
        {
            context.ScheduleAction(Body, "Leif", OnCompleted, OnFaulted);
        }

        private void OnCompleted(NativeActivityContext context, ActivityInstance completedInstance)
        {
            
        }

        private void OnFaulted(NativeActivityFaultContext faultContext, Exception propagatedException, ActivityInstance propagatedFrom)
        {
            throw new NotImplementedException();
        }

    }
}
