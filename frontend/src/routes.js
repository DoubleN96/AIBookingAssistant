// Soft UI Dashboard React layouts
import Dashboard from "layouts/dashboard";
import Maintanence from "layouts/maintanence";
import Commercial from "layouts/commercial";

// Soft UI Dashboard React icons
import Settings from "examples/Icons/Settings";
import Document from "examples/Icons/Document";
import SpaceShip from "examples/Icons/SpaceShip";
import CustomerSupport from "examples/Icons/CustomerSupport";
import CreditCard from "examples/Icons/CreditCard";

const routes = [
  {
    type: "collapse",
    name: "Dashboard",
    key: "dashboard",
    route: "/dashboard",
    icon: <SpaceShip size="12px" />,
    component: <Dashboard />,
    noCollapse: true,
  },
  {
    type: "collapse",
    name: "Maintanence",
    key: "maintanence",
    route: "/maintanence",
    icon: <Settings size="12px" />,
    component: <Maintanence />,
    noCollapse: true,
  },
  { type: "title", title: "Chat & KPI", key: "account-pages" },
  {
    type: "collapse",
    name: "Commercial",
    key: "commercial",
    route: "/commercial",
    icon: <CustomerSupport size="12px" />,
    component: <Commercial />,
    noCollapse: true,
  },
];

export default routes;
