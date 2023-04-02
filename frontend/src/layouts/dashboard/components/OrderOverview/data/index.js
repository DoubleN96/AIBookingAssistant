// @mui material components
import Tooltip from "@mui/material/Tooltip";
import SoftBadge from "components/SoftBadge";
import Grid from "@mui/material/Grid";
// Soft UI Dashboard React components
import SoftBox from "components/SoftBox";
import Bed from '@mui/icons-material/KingBedOutlined';
import Bathtub from '@mui/icons-material/BathtubOutlined';
import Shower from '@mui/icons-material/ShowerOutlined';
import Chair from '@mui/icons-material/ChairOutlined';
import Accessible from '@mui/icons-material/AccessibleOutlined';
import SoftTypography from "components/SoftTypography";
import SoftAvatar from "components/SoftAvatar";
import SoftStatus from "components/SoftStatus";
// Images
import homedecore1 from "assets/images/home-decor-1.jpg";
import homedecore2 from "assets/images/home-decor-2.jpg";
import homedecore3 from "assets/images/home-decor-3.jpg";

export default function data() {
  const avatars = (members) =>
    members.map(([image, name]) => (
      <Tooltip key={name} title={name} placeholder="bottom">
        <SoftAvatar
          src={image}
          alt="name"
          size="xxl"

        />
      </Tooltip>
    ));

  return {
    columns: [
      { name: "room", align: "center" },
      { name: "details", align: "center" },
      { name: "location", align: "center" },
      { name: "status", align: "center" },
    ],

    rows: [
      {
        room: (
          <SoftBox display="flex">
            {avatars([
              [homedecore1],
            ])}
          </SoftBox>
        ),
        details: (
          <SoftBox>
          <SoftTypography variant="h8" gutterBottom>
          <Bed fontSize="medium" /> 
          </SoftTypography>
          <SoftTypography variant="h8" gutterBottom>
          <Bathtub fontSize="medium"/> 
          </SoftTypography>
          <SoftTypography variant="h8" gutterBottom>
          <Accessible fontSize="medium"/> 
          </SoftTypography>
        </SoftBox>
        ),
        location: (
          <SoftBox>
          <SoftTypography variant="h8" gutterBottom>
          Kollwitzstraße 42, Berlin
          </SoftTypography>
        </SoftBox>
        ),
        status: (
          <SoftBadge variant="gradient" badgeContent="rented" color="secondary" size="xs" container />
        ),
      },
      {
        room: (
          <SoftBox display="flex">
            {avatars([
              [homedecore2],
            ])}
          </SoftBox>
        ),
    
        details: (
          <SoftBox>
          <SoftTypography variant="h8" gutterBottom>
          <Bed fontSize="medium" /> 
          </SoftTypography>
          <SoftTypography variant="h8" gutterBottom>
          <Chair fontSize="medium"/> 
          </SoftTypography>
          <SoftTypography variant="h8" gutterBottom>
          <Shower fontSize="medium"/> 
          </SoftTypography>
        </SoftBox>
        ),
        location: (
          <SoftBox>
          <SoftTypography variant="h8" gutterBottom>
            Dunrstraße 71, Stuttgart
          </SoftTypography>
        </SoftBox>
        ),
        status: (
          <SoftBadge variant="gradient" badgeContent="listed" color="success" size="xs" container />
        ),
      },
    ],
  };
}