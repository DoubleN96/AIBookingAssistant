//coded by Sandra Ashipala for Labláb AI hackathon 04.2023 <https://github.com/sandramsc>

/* eslint-disable react/prop-types */
// Soft UI Dashboard React components
import SoftBox from "components/SoftBox";
import SoftTypography from "components/SoftTypography";
import SoftAvatar from "components/SoftAvatar";
import SoftBadge from "components/SoftBadge";

// Soft UI Dashboard React components
import SoftButton from "components/SoftButton";
import SoftProgress from "components/SoftProgress";

// @mui material components
import Icon from "@mui/material/Icon";

function Completion({ value, color }) {
  return (
    <SoftBox display="flex" alignItems="center">
      <SoftTypography variant="caption" color="text" fontWeight="medium">
        {value}%&nbsp;
      </SoftTypography>
      <SoftBox width="4.65rem">
        <SoftProgress value={value} color={color} variant="gradient" label={false} />
      </SoftBox>
    </SoftBox>
  );
}

function Title({ name }) {
  return (
    <SoftBox display="flex" alignItems="center" px={1} py={0.5}>
      <SoftBox display="flex" flexDirection="column">
        <SoftTypography variant="button" fontWeight="medium">
          {name}
        </SoftTypography>
      </SoftBox>
    </SoftBox>
  );
}

function Issuer({ job }) {
  return (
    <SoftBox display="flex" flexDirection="column">
      <SoftTypography variant="caption" fontWeight="medium" color="text">
        {job}
      </SoftTypography>
    </SoftBox>
  );
}

function Property({ unit}) {
  return (
    <SoftBox display="flex" flexDirection="column">
      <SoftTypography variant="caption" fontWeight="medium" color="text">
        {unit}
      </SoftTypography>
    </SoftBox>
  );
}


const maintanenceTableData = {
  columns: [
    { name: "title", align: "left" },
    { name: "issuer", align: "left" },
    { name: "priority", align: "center" },
    { name: "property", align: "left" },
    { name: "status", align: "center" },
    { name: "reportedon", align: "center" },
    { name: "category", align: "center" },
    { name: "completion", align: "center" },
    { name: "delete", align: "center" },
    { name: "edit", align: "center" },
  ],

  rows: [
    {
      title: <Title name="Fix floor damage"   variant="caption"/>,
      issuer: <Issuer job="Rose Stanley"/>,
      priority: (
        <SoftBadge variant="gradient" badgeContent="critical" color="error" size="xs" container />
      ),
      property: <Property unit="Angelica Loaf 973"/>,
      status: (
        <SoftBadge variant="gradient" badgeContent="open" color="info" size="xs" container />
      ),
      reportedon: (
        <SoftTypography variant="caption" color="secondary" fontWeight="medium">
          23/04/18
        </SoftTypography>
      ),
      completion: <Completion value={45} color="warning" />,
      category: (
        <SoftTypography
          component="a"
          href="#"
          variant="caption"
          color="secondary"
          fontWeight="medium"
        >
          Flooring
        </SoftTypography>
      ),
      delete: (
        <SoftBox mr={1}>
        <SoftButton variant="text" color="error">
          <Icon>delete</Icon>
        </SoftButton>
      </SoftBox>
      ),
      edit: (
        <SoftButton variant="text" color="dark">
              <Icon>edit</Icon>
            </SoftButton>
      ),

    },
    {
      title: <Title  name="Fix Internet"  variant="caption"/>,
      issuer: <Issuer job="Amber Torres"/>,
      priority: (
        <SoftBadge variant="gradient" badgeContent="high" color="warning" size="xs" container />
      ),
      property: <Property unit="Lynette Motorway 628"/>,
      status: (
        <SoftBadge variant="gradient" badgeContent="closed" color="success" size="xs" container />
      ),
      reportedon: (
        <SoftTypography variant="caption" color="secondary" fontWeight="medium">
          11/01/19
        </SoftTypography>
      ),
      completion: <Completion value={100} color="success" />,
      category: (
        <SoftTypography
          component="a"
          href="#"
          variant="caption"
          color="secondary"
          fontWeight="medium"
        >
          Electrical
        </SoftTypography>
      ),
      delete: (
        <SoftBox mr={1}>
        <SoftButton variant="text" color="error">
          <Icon>delete</Icon>
        </SoftButton>
      </SoftBox>
      ),
      edit: (
        <SoftButton variant="text" color="dark">
              <Icon>edit</Icon>
            </SoftButton>
      ),
    },
    {
      title: <Title name="Fix heating issue"  variant="caption"/>,
      issuer: <Issuer job="Joy Barnes"/>,
      priority: (
        <SoftBadge variant="gradient" badgeContent="medium" color="secondary" size="xs" container />
      ),
      property: <Property unit="Melody Radial 889"/>,
      status: (
        <SoftBadge variant="gradient" badgeContent="open" color="info" size="xs" container />
      ),
      reportedon: (
        <SoftTypography variant="caption" color="secondary" fontWeight="medium">
          19/09/17
        </SoftTypography>
      ),
      completion: <Completion value={25} color="warning" />,
      category: (
        <SoftTypography
          component="a"
          href="#"
          variant="caption"
          color="secondary"
          fontWeight="medium"
        >
          Heating
        </SoftTypography>
      ),
      delete: (
        <SoftBox mr={1}>
        <SoftButton variant="text" color="error">
          <Icon>delete</Icon>
        </SoftButton>
      </SoftBox>
      ),
      edit: (
        <SoftButton variant="text" color="dark">
              <Icon>edit</Icon>
            </SoftButton>
      ),
    },
    {
      title: <Title name="Fix broken window"  variant="caption"/>,
      issuer: <Issuer job="Leon Peters"/>,
      priority: (
        <SoftBadge variant="gradient" badgeContent="medium" color="secondary" size="xs" container />
      ),
      property: <Property unit="Thiel Street 71101"/>,
      status: (
        <SoftBadge variant="gradient" badgeContent="closed" color="success" size="xs" container />
      ),
      reportedon: (
        <SoftTypography variant="caption" color="secondary" fontWeight="medium">
          24/12/08
        </SoftTypography>
      ),
      completion: <Completion value={100} color="success" />,
      category: (
        <SoftTypography
          component="a"
          href="#"
          variant="caption"
          color="secondary"
          fontWeight="medium"
        >
         Windows
        </SoftTypography>
      ),
      delete: (
        <SoftBox mr={1}>
        <SoftButton variant="text" color="error">
          <Icon>delete</Icon>
        </SoftButton>
      </SoftBox>
      ),
      edit: (
        <SoftButton variant="text" color="dark">
              <Icon>edit</Icon>
            </SoftButton>
      ),
    },
    {
      title: <Title name="Fix furniture damage"  variant="caption"/>,
      issuer: <Issuer job="Richard Gran"/>,
      priority: (
        <SoftBadge variant="gradient" badgeContent="critical" color="error" size="xs" container />
      ),
      property: <Property unit="Lubowitz Villages 8287"/>,
      status: (
        <SoftBadge variant="gradient" badgeContent="open" color="info" size="xs" container />
      ),
      reportedon: (
        <SoftTypography variant="caption" color="secondary" fontWeight="medium">
          04/10/21
        </SoftTypography>
      ),
      completion: <Completion value={89} color="info" />,
      category: (
        <SoftTypography
          component="a"
          href="#"
          variant="caption"
          color="secondary"
          fontWeight="medium"
        >
          Furniture
        </SoftTypography>
      ),
      delete: (
        <SoftBox mr={1}>
        <SoftButton variant="text" color="error">
          <Icon>delete</Icon>
        </SoftButton>
      </SoftBox>
      ),
      edit: (
        <SoftButton variant="text" color="dark">
              <Icon>edit</Icon>
            </SoftButton>
      ),
    },
  ],
};

export default maintanenceTableData;
