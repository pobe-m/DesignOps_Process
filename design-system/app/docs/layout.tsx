import { ModeToggle } from "@/components/layout/mode-toggle";
import { DocsSidebar } from "@/components/docs/docs-sidebar";
import { getNavGroups } from "@/components/docs/registry";
import { Separator } from "@/components/ui/separator";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";

export default function DocsLayout({ children }: { children: React.ReactNode }) {
  const groups = getNavGroups();

  return (
    <SidebarProvider>
      <DocsSidebar groups={groups} />
      <SidebarInset>
        <header className="bg-background/80 sticky top-0 z-10 flex h-14 items-center gap-2 border-b px-4 backdrop-blur">
          <SidebarTrigger className="-ml-1" />
          <Separator orientation="vertical" className="mr-2 h-4" />
          <span className="text-sm font-medium">Documentation</span>
          <div className="ml-auto">
            <ModeToggle />
          </div>
        </header>
        <div className="flex-1">{children}</div>
      </SidebarInset>
    </SidebarProvider>
  );
}
