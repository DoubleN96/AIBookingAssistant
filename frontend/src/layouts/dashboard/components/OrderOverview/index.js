import { useState } from "react";

// @mui material components
import Icon from "@mui/material/Icon";
import Card from "@mui/material/Card";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import SoftButton from "components/SoftButton";

// Soft UI Dashboard React components
import SoftBox from "components/SoftBox";
import SoftTypography from "components/SoftTypography";

// Soft UI Dashboard Materail-UI example components
import Table from "examples/Tables/Table";

// Data
import data from "layouts/dashboard/components/OrderOverview/data";

function OrderOverview() {
  const { columns, rows } = data();
  const [menu, setMenu] = useState(null);

  const openMenu = ({ currentTarget }) => setMenu(currentTarget);
  const closeMenu = () => setMenu(null);

  const renderMenu = (
    <Menu
      id="simple-menu"
      anchorEl={menu}
      anchorOrigin={{
        vertical: "top",
        horizontal: "left",
      }}
      transformOrigin={{
        vertical: "top",
        horizontal: "right",
      }}
      open={Boolean(menu)}
      onClose={closeMenu}
    >
    <MenuItem onClick={closeMenu}>View All</MenuItem>
    </Menu>
  );

  return (
    <Card >
      <SoftBox display="flex" justifyContent="space-between" alignItems="center" p={2}>
        <SoftBox>
          <SoftTypography variant="h6" gutterBottom>
            Connected Rooms
          </SoftTypography>
        </SoftBox>
        <SoftBox pt={2} px={2} display="flex" justifyContent="space-between" alignItems="center">
      </SoftBox>
        <SoftBox color="text" px={2}>
        <Icon sx={{ cursor: "pointer", fontWeight: "bold" }}  fontSize="small" onClick={openMenu}>
            more_vert
          </Icon>
        </SoftBox>
        {renderMenu}
      </SoftBox>

      <SoftBox
        sx={{
          "& .MuiTableRow-root:not(:last-child)": {
            "& td": {
              borderBottom: ({ borders: { borderWidth, borderColor } }) =>
                `${borderWidth[1]} solid ${borderColor}`,
            },
          },
        }}
      >
        <Table columns={columns} rows={rows} />
          

      </SoftBox>
      <SoftBox pt={1} pb={1} color="text" px={2}>
          <SoftButton variant="outlined" color="info" size="small">
         add room +
        </SoftButton>
        </SoftBox>
    </Card>
  );
}

export default OrderOverview;
