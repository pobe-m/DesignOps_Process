"use client";

import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Palette, Search } from "lucide-react";

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarInput,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "@/components/ui/sidebar";

type NavGroup = {
  title: string;
  items: { title: string; slug: string }[];
};

export function DocsSidebar({ groups }: { groups: NavGroup[] }) {
  const pathname = usePathname();
  const [query, setQuery] = React.useState("");

  const q = query.trim().toLowerCase();
  const filteredGroups = q
    ? groups
        .map((group) => ({
          ...group,
          items: group.items.filter(
            (item) =>
              item.title.toLowerCase().includes(q) ||
              item.slug.toLowerCase().includes(q),
          ),
        }))
        .filter((group) => group.items.length > 0)
    : groups;

  return (
    <Sidebar>
      <SidebarHeader className="gap-2 border-b">
        <Link
          href="/docs"
          className="flex items-center gap-2 px-2 py-1.5 font-semibold"
        >
          <span className="flex size-7 items-center justify-center rounded-md bg-primary text-primary-foreground">
            <Palette className="size-4" />
          </span>
          <span>Design System</span>
        </Link>
        <div className="relative px-2 pb-1">
          <Search className="text-muted-foreground pointer-events-none absolute top-1/2 left-4 size-4 -translate-y-1/2" />
          <SidebarInput
            type="search"
            placeholder="Search components…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            aria-label="Search components"
            className="pl-8"
          />
        </div>
      </SidebarHeader>

      <SidebarContent>
        {!q && (
          <SidebarGroup>
            <SidebarGroupLabel>Getting Started</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                <SidebarMenuItem>
                  <SidebarMenuButton asChild isActive={pathname === "/docs"}>
                    <Link href="/docs">Introduction</Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        )}

        {filteredGroups.length === 0 && (
          <p className="text-muted-foreground px-4 py-2 text-sm">
            No components found.
          </p>
        )}

        {filteredGroups.map((group) => (
          <SidebarGroup key={group.title}>
            <SidebarGroupLabel>{group.title}</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {group.items.map((item) => {
                  const href = `/docs/${item.slug}`;
                  return (
                    <SidebarMenuItem key={item.slug}>
                      <SidebarMenuButton asChild isActive={pathname === href}>
                        <Link href={href}>{item.title}</Link>
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  );
                })}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        ))}
      </SidebarContent>

      <SidebarRail />
    </Sidebar>
  );
}
