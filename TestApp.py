import resource
import streamlit as st
from streamlit_tags import st_tags
#st.session_state['resource_groups'] = []

#initialize variables
subnet1_name = None
subnet2_name = None
region = None
adf_name = None
vnet = None
vnet_rg = None
vnet_address_space = None

st.title('Sample Terraform App')

resource_groups = st_tags(
    label='Enter Resource Group Names (Up to 10):',
    text='Press enter to add more',
    maxtags = 10,
    key='1') 
if resource_groups:
  region = st.selectbox('Select Region:', ['eastus', 'westus'])

if region:
  vnet = st.text_input('VNet Name')
  vnet_rg = st.selectbox('Select VNet Resource Group', resource_groups)
  vnet_address_space = st.text_input('VNet Address Space', "10.0.0.0/16")
  if st.checkbox('Add Subnet 1'):
    subnet1_name = st.text_input('Subnet 1 Name')
    subnet1_rg = st.selectbox('Select Subnet 1 Resource Group', resource_groups)
    subnet1_address_space = st.text_input(f'{subnet1_name} Address Space', "10.0.1.0/24")
  if st.checkbox('Add Subnet 2'):
    subnet2_name = st.text_input('Subnet 2 Name')
    subnet2_rg = st.selectbox('Select Subnet 2 Resource Group', resource_groups)
    subnet2_address_space = st.text_input(f'{subnet2_name} Address Space', "10.0.2.0/24")
  if st.checkbox('Setup ADF'):
    adf_name = st.text_input('ADF Name (Must be Globally Unique)')
    adf_rg = st.selectbox('Select ADF Resource Group', resource_groups)


tf_main = """
terraform {
  \nrequired_providers {
    \nazurerm = {
      \nsource  = "hashicorp/azurerm"
      \nversion = "~> 2.65"
    \n}
  \n}

  \nrequired_version = ">= 1.1.0"
\n}

\nprovider "azurerm" {
  \nfeatures { }
\n }
"""
for num, rg in enumerate(resource_groups):
   tf_main += f"""
resource "azurerm_resource_group" "rg_{num}" {{
  \n name = "{rg}"
  \n location = "{region}"
\n }}
"""
#add the vnet
tf_main += f"""
resource "azurerm_virtual_network" "{vnet}" {{
  \n name                = "{vnet}"
  \n resource_group_name = azurerm_resource_group.{vnet_rg}.name
  \n location            = azurerm_resource_group.{vnet_rg}.location
  \n address_space       = ["{vnet_address_space}"]
\n }}
"""
if subnet1_name:
  tf_main += f"""
resource "azurerm_subnet" "{subnet1_name}" {{
  \n name                 = "{subnet1_name}"
  \n virtual_network_name = "{vnet}"
  \n resource_group_name = azurerm_resource_group.{vnet}.name
  \n address_prefixes     = ["{subnet1_address_space}"]
\n }}
"""
if subnet2_name:
  tf_main += f"""
resource "azurerm_subnet" "{subnet2_name}" {{
  \n name                 = "{subnet2_name}"
  \n virtual_network_name = "{vnet}"
  \n resource_group_name = azurerm_resource_group.{vnet}.name
  \n address_prefixes     = ["{subnet2_address_space}"]
\n }}
"""

if adf_name:
  tf_main += f"""
  resource "azurerm_data_factory" "{adf_name}" {{
  \n name                = "{adf_name}"
  \n resource_group_name = azurerm_resource_group.{adf_rg}.name
  \n location            = azurerm_resource_group.{adf_rg}.location
\n }}
"""
# main_tf_file = f"""
# terraform {{
#   required_providers {{
#     azurerm = {{
#       source  = "hashicorp/azurerm"
#       version = "~> 2.65"
#     }}
#   }}

#   required_version = ">= 1.1.0"
# }}

# provider "azurerm" {{
#   features {{}}
# }}

# resource "azurerm_resource_group" "rg" {{
#   name     = 
#   location = 
# }}
# """
gen_code = st.button('Generate Code')
if gen_code:
    st.write(gen_code)
    st.write(tf_main)