"""
DBBS Mod Collection

DBBS collection of NMODL assets

Glia asset bundle. If the Glia Asset Manager (`nmodl-glia`) is installed, the NMODL assets
in this package will automatically be available in your Glia library for use in the Arbor
and NEURON brain simulation engines.
"""
from pathlib import Path
from glia import Package, Mod

__version__ = "4.0.0b1"
package = Package(
    "dbbs_mod_collection",
    Path(__file__).resolve().parent,
    mods=[
        Mod("mods/AMPA__0.mod", "AMPA", is_point_process=True),
        Mod("mods/AMPA__granule.mod", "AMPA", variant="granule", is_point_process=True),
        Mod("mods/CaL13__0.mod", "CaL13"),
        Mod("mods/Ca__granule_cell.mod", "Ca", variant="granule_cell"),
        Mod("mods/Cav2_1__0.mod", "Cav2_1"),
        Mod("mods/Cav2_2__0.mod", "Cav2_2"),
        Mod("mods/Cav2_3__0.mod", "Cav2_3"),
        Mod("mods/Cav3_1__0.mod", "Cav3_1"),
        Mod("mods/Cav3_2__0.mod", "Cav3_2"),
        Mod("mods/Cav3_3__0.mod", "Cav3_3"),
        Mod("mods/GABA__0.mod", "GABA", is_point_process=True),
        Mod("mods/GABA__biexp.mod", "GABA", variant="biexp", is_point_process=True),
        Mod("mods/GABA__granule.mod", "GABA", variant="granule", is_point_process=True),
        Mod("mods/HCN1__0.mod", "HCN1"),
        Mod("mods/HCN1__golgi.mod", "HCN1", variant="golgi"),
        Mod("mods/HCN2__0.mod", "HCN2"),
        Mod("mods/Kca1_1__0.mod", "Kca1_1"),
        Mod("mods/Kca2_2__0.mod", "Kca2_2"),
        Mod("mods/Kca3_1__0.mod", "Kca3_1"),
        Mod("mods/Kir2_3__0.mod", "Kir2_3"),
        Mod("mods/Km__granule_cell.mod", "Km", variant="granule_cell"),
        Mod("mods/Kv1_1__0.mod", "Kv1_1"),
        Mod("mods/Kv1_5__0.mod", "Kv1_5"),
        Mod("mods/Kv2_2__0.mod", "Kv2_2"),
        Mod("mods/Kv3_3__0.mod", "Kv3_3"),
        Mod("mods/Kv3_4__0.mod", "Kv3_4"),
        Mod("mods/Kv4_3__0.mod", "Kv4_3"),
        Mod("mods/Kv7__0.mod", "Kv7"),
        Mod("mods/Leak__0.mod", "Leak"),
        Mod("mods/Leak__GABA.mod", "Leak", variant="GABA"),
        Mod("mods/NMDA__granule.mod", "NMDA", variant="granule", is_point_process=True),
        Mod(
            "mods/NMDA__stellate.mod", "NMDA", variant="stellate", is_point_process=True
        ),
        Mod("mods/Na__granule_cell.mod", "Na", variant="granule_cell"),
        Mod("mods/Na__granule_cell_FHF.mod", "Na", variant="granule_cell_FHF"),
        Mod("mods/Nav1_1__0.mod", "Nav1_1"),
        Mod("mods/Nav1_6__0.mod", "Nav1_6"),
        Mod("mods/cdp5__0.mod", "cdp5"),
        Mod("mods/cdp5__CAM.mod", "cdp5", variant="CAM"),
        Mod("mods/cdp5__CAM_GoC.mod", "cdp5", variant="CAM_GoC"),
        Mod("mods/cdp5__CR.mod", "cdp5", variant="CR"),
        Mod("mods/gap_junction__0.mod", "gap_junction", is_point_process=True),
        Mod(
            "mods/gap_junction__parallel.mod",
            "gap_junction",
            variant="parallel",
            is_point_process=True,
        ),
    ],
)
