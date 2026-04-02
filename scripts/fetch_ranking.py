"""
RAPTOR Ranking Engine
Scarica 714 ticker da Yahoo Finance, calcola indicatori e scrive data/ranking.json
"""
import json, os, math
from datetime import datetime, timezone
import yfinance as yf
import numpy as np

# ── TICKERS ────────────────────────────────────────────────
TICKERS = [
    {"y":"AFK","c":"top4 logical usa","t":"AFK"},{"y":"ARGT","c":"top4 logical usa","t":"ARGT"},
    {"y":"ASHR","c":"top4 logical usa","t":"ASHR"},{"y":"DIA","c":"top4 logical usa","t":"DIA"},
    {"y":"ECH","c":"top4 logical usa","t":"ECH"},{"y":"EEM","c":"top4 logical usa","t":"EEM"},
    {"y":"IAEX.AS","c":"Paesi","t":"IAEX"},{"y":"TOF.AS","c":"ATTIVO_MOMENT_DIVIDEND_SMALL_ETFETF","t":"TOF"},
    {"y":"18MN.DE","c":"Lazy_Portfolio","t":"18MN"},{"y":"7USH.DE","c":"BOND","t":"7USH"},
    {"y":"CBUH.DE","c":"ATTIVO_MOMENT_DIVIDEND_SMALL_ETFETF","t":"CBUH"},{"y":"CEB1.DE","c":"BOND","t":"CEB1"},
    {"y":"CEB4.DE","c":"NEW AREA, Paesi","t":"CEB4"},{"y":"DBZB.DE","c":"Lazy_Portfolio","t":"DBZB"},
    {"y":"EUNY.DE","c":"ATTIVO_MOMENT_DIVIDEND_SMALL_ETFETF","t":"EUNY"},{"y":"IBC5.DE","c":"BOND","t":"IBC5"},
    {"y":"IBCJ.DE","c":"Paesi","t":"IBCJ"},{"y":"IQQ9.DE","c":"NEW AREA, Paesi","t":"IQQ9"},
    {"y":"IQQF.DE","c":"NEW AREA, Paesi","t":"IQQF"},{"y":"IS04.DE","c":"BOND","t":"IS04"},
    {"y":"IS3C.DE","c":"Lazy_Portfolio","t":"IS3C"},{"y":"IS3N.DE","c":"Lazy_Portfolio","t":"IS3N"},
    {"y":"IS3U.DE","c":"Paesi","t":"IS3U"},{"y":"ISPA.DE","c":"ATTIVO_MOMENT_DIVIDEND_SMALL_ETFETF","t":"ISPA"},
    {"y":"IUSQ.DE","c":"Lazy_Portfolio","t":"IUSQ"},{"y":"IUSS.DE","c":"Paesi","t":"IUSS"},
    {"y":"LCUJ.DE","c":"Lazy_Portfolio","t":"LCUJ"},{"y":"MJMT.DE","c":"ATTIVO_MOMENT_DIVIDEND_SMALL_ETFETF","t":"MJMT"},
    {"y":"QDVA.DE","c":"ATTIVO_MOMENT_DIVIDEND_SMALL_ETFETF","t":"QDVA"},{"y":"SPP5.DE","c":"BOND","t":"SPP5"},
    {"y":"SPYX.DE","c":"ATTIVO_MOMENT_DIVIDEND_SMALL_ETFETF","t":"SPYX"},{"y":"SXR1.DE","c":"Lazy_Portfolio","t":"SXR1"},
    {"y":"SXRT.DE","c":"Lazy_Portfolio","t":"SXRT"},{"y":"SXRU.DE","c":"NEW AREA, Paesi","t":"SXRU"},
    {"y":"SXRW.DE","c":"Lazy_Portfolio","t":"SXRW"},{"y":"VGWE.DE","c":"ATTIVO_MOMENT_DIVIDEND_SMALL_ETFETF","t":"VGWE"},
    {"y":"VUKG.DE","c":"Paesi","t":"VUKG"},{"y":"XBAS.DE","c":"Paesi","t":"XBAS"},
    {"y":"XCS3.DE","c":"Paesi","t":"XCS3"},{"y":"XCS4.DE","c":"Paesi","t":"XCS4"},
    {"y":"XD9E.DE","c":"Lazy_Portfolio","t":"XD9E"},{"y":"XD9U.DE","c":"Lazy_Portfolio","t":"XD9U"},
    {"y":"XDEM.DE","c":"ATTIVO_MOMENT_DIVIDEND_SMALL_ETFETF","t":"XDEM"},{"y":"XESD.DE","c":"Paesi","t":"XESD"},
    {"y":"XGIN.DE","c":"Lazy_Portfolio","t":"XGIN"},{"y":"XMKA.DE","c":"Paesi","t":"XMKA"},
    {"y":"XPQP.DE","c":"Paesi","t":"XPQP"},{"y":"XWEM.DE","c":"ATTIVO_MOMENT_DIVIDEND_SMALL_ETFETF","t":"XWEM"},
    {"y":"IVAI.MI","c":"Tematici","t":"IVAI"},{"y":"IVDF.DE","c":"Tematici","t":"IVDF"},
    {"y":"A01U.MI","c":"BOND","t":"A01U"},{"y":"ACT20.MI","c":"ATTIVO_MOMENT_DIVIDEND_SMALL_ETFETF","t":"ACT20"},
    {"y":"ACT60.MI","c":"ATTIVO_MOMENT_DIVIDEND_SMALL_ETFETF","t":"ACT60"},{"y":"ACTEQ.MI","c":"ATTIVO_MOMENT_DIVIDEND_SMALL_ETFETF","t":"ACTEQ"},
    {"y":"ADLU.MI","c":"BOND","t":"ADLU"},{"y":"AEGE.MI","c":"BOND","t":"AEGE"},
    {"y":"AGEB.MI","c":"BOND","t":"AGEB"},{"y":"AGED.MI","c":"Tematici","t":"AGED"},
    {"y":"AGGH.MI","c":"BOND","t":"AGGH"},{"y":"AI4UJ.MI","c":"Tematici","t":"AI4UJ"},
    {"y":"AIAA.MI","c":"Tematici","t":"AIAA"},{"y":"AIAI.MI","c":"Tematici","t":"AIAI"},
    {"y":"AICU.MI","c":"BOND","t":"AICU"},{"y":"AIGA.MI","c":"Materie","t":"AIGA"},
    {"y":"AIGC.MI","c":"Materie","t":"AIGC"},{"y":"AIGE.MI","c":"Materie","t":"AIGE"},
    {"y":"AIGG.MI","c":"Materie","t":"AIGG"},{"y":"AIGI.MI","c":"Materie","t":"AIGI"},
    {"y":"AIGL.MI","c":"Materie","t":"AIGL"},{"y":"AIGO.MI","c":"Materie","t":"AIGO"},
    {"y":"AIGP.MI","c":"Materie","t":"AIGP"},{"y":"AIGS.MI","c":"Materie","t":"AIGS"},
    {"y":"AINF.MI","c":"Tematici","t":"AINF"},{"y":"AIQE.MI","c":"Tematici","t":"AIQE"},
    {"y":"ALAT.MI","c":"NEW AREA, Paesi","t":"ALAT"},{"y":"ALUM.MI","c":"Materie","t":"ALUM"},
    {"y":"ANAU.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"ANAU"},{"y":"AQWA.MI","c":"Tematici","t":"AQWA"},
    {"y":"ARMI.MI","c":"Tematici","t":"ARMI"},{"y":"ARMR.MI","c":"Tematici","t":"ARMR"},
    {"y":"ASRD.MI","c":"BOND","t":"ASRD"},{"y":"AT1.MI","c":"BOND","t":"AT1"},
    {"y":"AUCO.MI","c":"Tematici","t":"AUCO"},{"y":"AUHEUA.MI","c":"Paesi","t":"AUHEUA"},
    {"y":"BATT.MI","c":"Tematici","t":"BATT"},{"y":"BBTR.MI","c":"BOND","t":"BBTR"},
    {"y":"BCHN.MI","c":"Settoriali","t":"BCHN"},{"y":"BENE.MI","c":"Materie","t":"BENE"},
    {"y":"BIODV.MI","c":"Settoriali","t":"BIODV"},{"y":"BIOT.MI","c":"Tematici","t":"BIOT"},
    {"y":"BKCH.MI","c":"Tematici","t":"BKCH"},{"y":"BLTH.MI","c":"Tematici","t":"BLTH"},
    {"y":"BNK.MI","c":"Settoriali","t":"BNK"},{"y":"BNKE.MI","c":"Settoriali","t":"BNKE"},
    {"y":"BOTZ.MI","c":"Tematici","t":"BOTZ"},{"y":"BRENT.MI","c":"Materie","t":"BRENT"},
    {"y":"BRES.MI","c":"Settoriali","t":"BRES"},{"y":"BRIJ.MI","c":"Tematici","t":"BRIJ"},
    {"y":"BRND.MI","c":"Materie","t":"BRND"},{"y":"BRNT.MI","c":"Materie","t":"BRNT"},
    {"y":"BTC.MI","c":"Tematici","t":"BTC"},{"y":"BTECH.MI","c":"Tematici","t":"BTECH"},
    {"y":"BUG.MI","c":"Tematici","t":"BUG"},{"y":"CAHEUA.MI","c":"NEW AREA, Paesi","t":"CAHEUA"},
    {"y":"CARB.MI","c":"Materie","t":"CARB"},{"y":"CAUT.MI","c":"Tematici","t":"CAUT"},
    {"y":"CCEUAS.MI","c":"Materie","t":"CCEUAS"},{"y":"CCUSAS.MI","c":"Materie","t":"CCUSAS"},
    {"y":"CHIP.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"CHIP"},{"y":"CHM.MI","c":"Settoriali","t":"CHM"},
    {"y":"CIBR.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"CIBR"},{"y":"CIT.MI","c":"Tematici","t":"CIT"},
    {"y":"CITE.MI","c":"Tematici","t":"CITE"},{"y":"CITY.MI","c":"Tematici","t":"CITY"},
    {"y":"CLIP.MI","c":"BOND","t":"CLIP"},{"y":"CLOU.MI","c":"Tematici","t":"CLOU"},
    {"y":"CMOC.MI","c":"Materie","t":"CMOC"},{"y":"CMOD.MI","c":"Materie","t":"CMOD"},
    {"y":"CMOE.MI","c":"Materie","t":"CMOE"},{"y":"CN1.MI","c":"Paesi","t":"CN1"},
    {"y":"CO2.MI","c":"Materie","t":"CO2"},{"y":"COCO.MI","c":"Materie","t":"COCO"},
    {"y":"COFF.MI","c":"Materie","t":"COFF"},{"y":"COMF.MI","c":"Materie","t":"COMF"},
    {"y":"COMH.MI","c":"Materie","t":"COMH"},{"y":"COMO.MI","c":"Materie","t":"COMO"},
    {"y":"COPA.MI","c":"Materie","t":"COPA"},{"y":"COPM.MI","c":"Tematici","t":"COPM"},
    {"y":"COPR.MI","c":"Tematici","t":"COPR"},{"y":"COPX.MI","c":"Tematici","t":"COPX"},
    {"y":"CORN.MI","c":"Materie","t":"CORN"},{"y":"COTN.MI","c":"Materie","t":"COTN"},
    {"y":"CROP.MI","c":"Tematici","t":"CROP"},{"y":"CRRY.MI","c":"Materie","t":"CRRY"},
    {"y":"CRUD.MI","c":"Materie","t":"CRUD"},{"y":"CSCA.MI","c":"NEW AREA, Paesi","t":"CSCA"},
    {"y":"CSEMAS.MI","c":"NEW AREA, Paesi","t":"CSEMAS"},{"y":"CSMIB.MI","c":"Paesi","t":"CSMIB"},
    {"y":"CSNDX.MI","c":"Paesi","t":"CSNDX"},{"y":"CSPXJ.MI","c":"NEW AREA, Paesi","t":"CSPXJ"},
    {"y":"CSSPX.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"CSSPX"},{"y":"CSUS.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"CSUS"},
    {"y":"CSUSS.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"CSUSS"},{"y":"CTEK.MI","c":"Tematici","t":"CTEK"},
    {"y":"CURE.MI","c":"Tematici","t":"CURE"},{"y":"CWE.MI","c":"Settoriali","t":"CWE"},
    {"y":"CYBO.MI","c":"Tematici","t":"CYBO"},{"y":"CYBR.MI","c":"Settoriali","t":"CYBR"},
    {"y":"DAPP.MI","c":"Tematici","t":"DAPP"},{"y":"DEFS.MI","c":"Settoriali","t":"DEFS"},
    {"y":"DFND.MI","c":"Tematici","t":"DFND"},{"y":"DFNS.MI","c":"Tematici","t":"DFNS"},
    {"y":"DGTL.MI","c":"Tematici","t":"DGTL"},{"y":"DISW.MI","c":"Settoriali","t":"DISW"},
    {"y":"DJE.MI","c":"Paesi","t":"DJE"},{"y":"DMAT.MI","c":"Tematici","t":"DMAT"},
    {"y":"DOCT.MI","c":"Tematici","t":"DOCT"},{"y":"DPAY.MI","c":"Tematici","t":"DPAY"},
    {"y":"DRVE.MI","c":"Tematici","t":"DRVE"},{"y":"EALU.MI","c":"Materie","t":"EALU"},
    {"y":"EBIZ.MI","c":"Tematici","t":"EBIZ"},{"y":"EBRT.MI","c":"Materie","t":"EBRT"},
    {"y":"EBUY.MI","c":"Tematici","t":"EBUY"},{"y":"ECAR.MI","c":"Tematici","t":"ECAR"},
    {"y":"ECEH.MI","c":"Materie","t":"ECEH"},{"y":"ECOF.MI","c":"Materie","t":"ECOF"},
    {"y":"ECOM.MI","c":"Tematici","t":"ECOM"},{"y":"ECOP.MI","c":"Materie","t":"ECOP"},
    {"y":"ECRD.MI","c":"Materie","t":"ECRD"},{"y":"ECRN.MI","c":"Materie","t":"ECRN"},
    {"y":"ECTN.MI","c":"Materie","t":"ECTN"},{"y":"EDOC.MI","c":"Tematici","t":"EDOC"},
    {"y":"EEA.MI","c":"Tematici","t":"EEA"},{"y":"EENG.MI","c":"Settoriali","t":"EENG"},
    {"y":"EFCM.MI","c":"Materie","t":"EFCM"},{"y":"EGEHE.MI","c":"Settoriali","t":"EGEHE"},
    {"y":"EIMI.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"EIMI"},{"y":"EIMT.MI","c":"Materie","t":"EIMT"},
    {"y":"ELCR.MI","c":"Tematici","t":"ELCR"},{"y":"EMOVE.MI","c":"Tematici","t":"EMOVE"},
    {"y":"EMOVJ.MI","c":"Tematici","t":"EMOVJ"},{"y":"EMQQ.MI","c":"Settoriali","t":"EMQQ"},
    {"y":"ENCO.MI","c":"Materie","t":"ENCO"},{"y":"ENERW.MI","c":"Settoriali","t":"ENERW"},
    {"y":"ENGS.MI","c":"Materie","t":"ENGS"},{"y":"ENIK.MI","c":"Materie","t":"ENIK"},
    {"y":"ENRG.MI","c":"Settoriali","t":"ENRG"},{"y":"ENTR.MI","c":"Materie","t":"ENTR"},
    {"y":"EPRA.MI","c":"Tematici","t":"EPRA"},{"y":"EPRE.MI","c":"Tematici","t":"EPRE"},
    {"y":"EROX.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"EROX"},{"y":"ESGO.MI","c":"Tematici","t":"ESGO"},
    {"y":"ESOY.MI","c":"Materie","t":"ESOY"},{"y":"ESPO.MI","c":"Tematici","t":"ESPO"},
    {"y":"ESPY.MI","c":"Tematici","t":"ESPY"},{"y":"EST.MI","c":"NEW AREA, Paesi","t":"EST"},
    {"y":"ESUG.MI","c":"Materie","t":"ESUG"},{"y":"EWAT.MI","c":"Materie","t":"EWAT"},
    {"y":"EXS1.MI","c":"Paesi","t":"EXS1"},{"y":"EXXY.MI","c":"Materie","t":"EXXY"},
    {"y":"EZNC.MI","c":"Materie","t":"EZNC"},{"y":"FAMAMW.MI","c":"Tematici","t":"FAMAMW"},
    {"y":"FAMMAI.MI","c":"Tematici","t":"FAMMAI"},{"y":"FAMMWF.MI","c":"Tematici","t":"FAMMWF"},
    {"y":"FAMMWS.MI","c":"Tematici","t":"FAMMWS"},{"y":"FAMTEL.MI","c":"Tematici","t":"FAMTEL"},
    {"y":"FAMWCS.MI","c":"Tematici","t":"FAMWCS"},{"y":"FCRU.MI","c":"Materie","t":"FCRU"},
    {"y":"FINSW.MI","c":"Settoriali","t":"FINSW"},{"y":"FINX.MI","c":"Tematici","t":"FINX"},
    {"y":"FLXI.MI","c":"Paesi","t":"FLXI"},{"y":"FLXT.MI","c":"Paesi","t":"FLXT"},
    {"y":"FLXU.MI","c":"Paesi","t":"FLXU"},{"y":"FMI.MI","c":"Paesi","t":"FMI"},
    {"y":"FOFD.MI","c":"Tematici","t":"FOFD"},{"y":"FOO.MI","c":"Settoriali","t":"FOO"},
    {"y":"FOOD.MI","c":"Settoriali","t":"FOOD"},{"y":"GAS.MI","c":"Materie","t":"GAS"},
    {"y":"GCLE.MI","c":"Tematici","t":"GCLE"},{"y":"GDIG.MI","c":"Tematici","t":"GDIG"},
    {"y":"GDX.MI","c":"Tematici","t":"GDX"},{"y":"GDXJ.MI","c":"Tematici","t":"GDXJ"},
    {"y":"GENDEE.MI","c":"Tematici","t":"GENDEE"},{"y":"GLUG.MI","c":"Tematici","t":"GLUG"},
    {"y":"GLUX.MI","c":"Tematici","t":"GLUX"},{"y":"GNOM.MI","c":"Tematici","t":"GNOM"},
    {"y":"GOAI.MI","c":"Tematici","t":"GOAI"},{"y":"GRC.MI","c":"Paesi","t":"GRC"},
    {"y":"GRCTB.MI","c":"Settoriali","t":"GRCTB"},{"y":"GREAL.MI","c":"Settoriali","t":"GREAL"},
    {"y":"GSCE.MI","c":"Materie","t":"GSCE"},{"y":"GSM.MI","c":"Tematici","t":"GSM"},
    {"y":"HDRO.MI","c":"Tematici","t":"HDRO"},{"y":"HEAL.MI","c":"Tematici","t":"HEAL"},
    {"y":"HERU.MI","c":"Tematici","t":"HERU"},{"y":"HLT.MI","c":"Settoriali","t":"HLT"},
    {"y":"HLTW.MI","c":"Settoriali","t":"HLTW"},{"y":"HNSC.MI","c":"Tematici","t":"HNSC"},
    {"y":"HPNA.MI","c":"Settoriali","t":"HPNA"},{"y":"HSTE.MI","c":"Paesi","t":"HSTE"},
    {"y":"HTWO.MI","c":"Tematici","t":"HTWO"},{"y":"HYDE.MI","c":"Tematici","t":"HYDE"},
    {"y":"HYGN.MI","c":"Tematici","t":"HYGN"},{"y":"HYLD.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"HYLD"},
    {"y":"IAPD.MI","c":"NEW AREA, Paesi","t":"IAPD"},{"y":"IBZL.MI","c":"Paesi","t":"IBZL"},
    {"y":"ICBR.MI","c":"Tematici","t":"ICBR"},{"y":"IEMB.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"IEMB"},
    {"y":"IJPE.MI","c":"NEW AREA, Paesi","t":"IJPE"},{"y":"IMIB.MI","c":"Paesi","t":"IMIB"},
    {"y":"INDG.MI","c":"Settoriali","t":"INDG"},{"y":"INDGW.MI","c":"Settoriali","t":"INDGW"},
    {"y":"INDI.MI","c":"Paesi","t":"INDI"},{"y":"INDO.MI","c":"Paesi","t":"INDO"},
    {"y":"INQQ.MI","c":"Tematici","t":"INQQ"},{"y":"INS.MI","c":"Settoriali","t":"INS"},
    {"y":"ISAC.MI","c":"NEW AREA, Paesi","t":"ISAC"},{"y":"ISAG.MI","c":"Tematici","t":"ISAG"},
    {"y":"ISPY.MI","c":"Tematici","t":"ISPY"},{"y":"IUSE.MI","c":"NEW AREA, Paesi","t":"IUSE"},
    {"y":"IWDE.MI","c":"NEW AREA, Paesi","t":"IWDE"},{"y":"IWVL.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"IWVL"},
    {"y":"JEDI.MI","c":"Tematici","t":"JEDI"},{"y":"JRGE.MI","c":"NEW AREA, Paesi","t":"JRGE"},
    {"y":"KARS.MI","c":"Settoriali","t":"KARS"},{"y":"KOR.MI","c":"Paesi","t":"KOR"},
    {"y":"KRBN.MI","c":"Materie","t":"KRBN"},{"y":"KWBE.MI","c":"Tematici","t":"KWBE"},
    {"y":"LABL.MI","c":"Tematici","t":"LABL"},{"y":"LAFRI.MI","c":"NEW AREA, Paesi","t":"LAFRI"},
    {"y":"LCCN.MI","c":"Paesi","t":"LCCN"},{"y":"LEAD.MI","c":"Materie","t":"LEAD"},
    {"y":"LGUS.MI","c":"Paesi","t":"LGUS"},{"y":"LINXB.MI","c":"ATTIVO_MOMENT_DIVIDEND_SMALL_ETFETF","t":"LINXB"},
    {"y":"LITM.MI","c":"Tematici","t":"LITM"},{"y":"LITU.MI","c":"Tematici","t":"LITU"},
    {"y":"LOCK.MI","c":"Tematici","t":"LOCK"},{"y":"LTAM.MI","c":"NEW AREA, Paesi","t":"LTAM"},
    {"y":"LVO.MI","c":"Materie","t":"LVO"},{"y":"MATW.MI","c":"Settoriali","t":"MATW"},
    {"y":"MCHN.MI","c":"Paesi","t":"MCHN"},{"y":"MCHT.MI","c":"Tematici","t":"MCHT"},
    {"y":"META.MI","c":"Materie","t":"META"},{"y":"METAA.MI","c":"Tematici","t":"METAA"},
    {"y":"METAJ.MI","c":"Tematici","t":"METAJ"},{"y":"METE.MI","c":"Tematici","t":"METE"},
    {"y":"METL.MI","c":"Tematici","t":"METL"},{"y":"MILL.MI","c":"Tematici","t":"MILL"},
    {"y":"MLPS.MI","c":"Tematici","t":"MLPS"},{"y":"MTAV.MI","c":"Tematici","t":"MTAV"},
    {"y":"MTVS.MI","c":"Tematici","t":"MTVS"},{"y":"NATO.MI","c":"Settoriali","t":"NATO"},
    {"y":"NCLR.MI","c":"Tematici","t":"NCLR"},{"y":"NGAS.MI","c":"Materie","t":"NGAS"},
    {"y":"NICK.MI","c":"Materie","t":"NICK"},{"y":"NRJC.MI","c":"Tematici","t":"NRJC"},
    {"y":"NUCL.MI","c":"Tematici","t":"NUCL"},{"y":"OCEAN.MI","c":"Settoriali","t":"OCEAN"},
    {"y":"OIH.MI","c":"Tematici","t":"OIH"},{"y":"PAVE.MI","c":"Tematici","t":"PAVE"},
    {"y":"PCOM.MI","c":"Materie","t":"PCOM"},{"y":"PHAG.MI","c":"Materie","t":"PHAG"},
    {"y":"PHPD.MI","c":"Materie","t":"PHPD"},{"y":"PHPM.MI","c":"Materie","t":"PHPM"},
    {"y":"PHPT.MI","c":"Materie","t":"PHPT"},{"y":"QNTM.MI","c":"Tematici","t":"QNTM"},
    {"y":"QTOP.MI","c":"Paesi","t":"QTOP"},{"y":"QUAD.MI","c":"Tematici","t":"QUAD"},
    {"y":"RARE.MI","c":"Tematici","t":"RARE"},{"y":"RAYZ.MI","c":"Tematici","t":"RAYZ"},
    {"y":"RBOT.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"RBOT"},{"y":"REMX.MI","c":"Tematici","t":"REMX"},
    {"y":"RENW.MI","c":"Tematici","t":"RENW"},{"y":"REUS.MI","c":"Tematici","t":"REUS"},
    {"y":"REUSE.MI","c":"Settoriali","t":"REUSE"},{"y":"RNRG.MI","c":"Tematici","t":"RNRG"},
    {"y":"ROBO.MI","c":"Tematici","t":"ROBO"},{"y":"ROE.MI","c":"Tematici","t":"ROE"},
    {"y":"SAUDI.MI","c":"Paesi","t":"SAUDI"},{"y":"SAUS.MI","c":"Paesi","t":"SAUS"},
    {"y":"SBIO.MI","c":"Settoriali","t":"SBIO"},{"y":"SCITY.MI","c":"Tematici","t":"SCITY"},
    {"y":"SEMA.MI","c":"NEW AREA, Paesi","t":"SEMA"},{"y":"SEME.MI","c":"Tematici","t":"SEME"},
    {"y":"SGBS.MI","c":"Materie","t":"SGBS"},{"y":"SILV.MI","c":"Tematici","t":"SILV"},
    {"y":"SJPA.MI","c":"NEW AREA, Paesi","t":"SJPA"},{"y":"SMCX.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"SMCX"},
    {"y":"SMEA.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"SMEA"},{"y":"SMH.MI","c":"Tematici","t":"SMH"},
    {"y":"SNSR.MI","c":"Tematici","t":"SNSR"},{"y":"SOLR.MI","c":"Tematici","t":"SOLR"},
    {"y":"SOYB.MI","c":"Materie","t":"SOYB"},{"y":"SOYO.MI","c":"Materie","t":"SOYO"},
    {"y":"SP1E.MI","c":"Paesi","t":"SP1E"},{"y":"SP5A.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"SP5A"},
    {"y":"SPXE.MI","c":"Paesi","t":"SPXE"},{"y":"SPXJ.MI","c":"Paesi","t":"SPXJ"},
    {"y":"SPY5.MI","c":"Paesi","t":"SPY5"},{"y":"SRSA.MI","c":"Paesi","t":"SRSA"},
    {"y":"STAW.MI","c":"Settoriali","t":"STAW"},{"y":"DFSV.DE","c":"Settoriali SPDR EURO","t":"DFSV"},
    {"y":"STKX.MI","c":"Settoriali SPDR EURO","t":"STKX"},{"y":"STNX.MI","c":"Settoriali SPDR EURO","t":"STNX"},
    {"y":"STPX.MI","c":"Settoriali SPDR EURO","t":"STPX"},{"y":"STQX.MI","c":"Settoriali SPDR EURO","t":"STQX"},
    {"y":"STRX.MI","c":"Settoriali SPDR EURO","t":"STRX"},{"y":"STSX.MI","c":"Settoriali SPDR EURO","t":"STSX"},
    {"y":"STTX.MI","c":"Settoriali SPDR EURO","t":"STTX"},{"y":"STUX.MI","c":"Settoriali SPDR EURO","t":"STUX"},
    {"y":"SUGA.MI","c":"Materie","t":"SUGA"},{"y":"SWDA.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"SWDA"},
    {"y":"SXLB.MI","c":"Settoriali SPDR USA","t":"SXLB"},{"y":"SXLC.MI","c":"Settoriali SPDR USA","t":"SXLC"},
    {"y":"SXLF.MI","c":"Settoriali SPDR USA","t":"SXLF"},{"y":"SXLI.MI","c":"Settoriali SPDR USA","t":"SXLI"},
    {"y":"SXLK.MI","c":"Settoriali SPDR USA","t":"SXLK"},{"y":"SXLP.MI","c":"Settoriali SPDR USA","t":"SXLP"},
    {"y":"SXLU.MI","c":"Settoriali SPDR USA","t":"SXLU"},{"y":"SXLV.MI","c":"Settoriali SPDR USA","t":"SXLV"},
    {"y":"SXLY.MI","c":"Settoriali SPDR USA","t":"SXLY"},{"y":"TELE.MI","c":"Settoriali","t":"TELE"},
    {"y":"TELEW.MI","c":"Settoriali","t":"TELEW"},{"y":"TLCO.MI","c":"Tematici","t":"TLCO"},
    {"y":"TNO.MI","c":"Settoriali","t":"TNO"},{"y":"TNOW.MI","c":"Settoriali","t":"TNOW"},
    {"y":"TRVL.MI","c":"Settoriali","t":"TRVL"},{"y":"TTFW.MI","c":"Materie","t":"TTFW"},
    {"y":"TUR.MI","c":"Paesi","t":"TUR"},{"y":"U3O8.MI","c":"Tematici","t":"U3O8"},
    {"y":"UGAS.MI","c":"Materie","t":"UGAS"},{"y":"UKE.MI","c":"Paesi","t":"UKE"},
    {"y":"UNIC.MI","c":"Tematici","t":"UNIC"},{"y":"URNJ.MI","c":"Tematici","t":"URNJ"},
    {"y":"URNU.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"URNU"},{"y":"USTEC.MI","c":"Tematici","t":"USTEC"},
    {"y":"UTI.MI","c":"Settoriali","t":"UTI"},{"y":"UTIW.MI","c":"Settoriali","t":"UTIW"},
    {"y":"VEGI.MI","c":"Tematici","t":"VEGI"},{"y":"VITA.MI","c":"Settoriali","t":"VITA"},
    {"y":"VITU.MI","c":"Settoriali","t":"VITU"},{"y":"VJPE.MI","c":"Paesi","t":"VJPE"},
    {"y":"VOLT.MI","c":"Tematici","t":"VOLT"},{"y":"VPN.MI","c":"Tematici","t":"VPN"},
    {"y":"VUKE.MI","c":"Paesi","t":"VUKE"},{"y":"VUSA.MI","c":"Paesi","t":"VUSA"},
    {"y":"WATC.MI","c":"Tematici","t":"WATC"},{"y":"WATT.MI","c":"Materie","t":"WATT"},
    {"y":"WBLK.MI","c":"Tematici","t":"WBLK"},{"y":"WCBR.MI","c":"Tematici","t":"WCBR"},
    {"y":"WCCA.MI","c":"Materie","t":"WCCA"},{"y":"WCLD.MI","c":"Settoriali","t":"WCLD"},
    {"y":"WCOA.MI","c":"Materie","t":"WCOA"},{"y":"WCOD.MI","c":"Settoriali SPDR WORLD","t":"WCOD"},
    {"y":"WCOE.MI","c":"Materie","t":"WCOE"},{"y":"WCOS.MI","c":"Settoriali SPDR WORLD","t":"WCOS"},
    {"y":"WDEF.MI","c":"Tematici","t":"WDEF"},{"y":"WDNA.MI","c":"Tematici","t":"WDNA"},
    {"y":"WEAT.MI","c":"Materie","t":"WEAT"},{"y":"WEB3.MI","c":"Tematici","t":"WEB3"},
    {"y":"WENT.MI","c":"Materie","t":"WENT"},{"y":"WENU.MI","c":"Materie","t":"WENU"},
    {"y":"WFIN.MI","c":"Settoriali SPDR WORLD","t":"WFIN"},{"y":"WGRO.MI","c":"Tematici","t":"WGRO"},
    {"y":"WHEA.MI","c":"Settoriali SPDR WORLD","t":"WHEA"},{"y":"WIND.MI","c":"Settoriali SPDR WORLD","t":"WIND"},
    {"y":"WMAT.MI","c":"Settoriali SPDR WORLD","t":"WMAT"},{"y":"WMGT.MI","c":"Tematici","t":"WMGT"},
    {"y":"WNDE.MI","c":"Tematici","t":"WNDE"},{"y":"WNDY.MI","c":"Tematici","t":"WNDY"},
    {"y":"WNRG.MI","c":"Settoriali SPDR WORLD","t":"WNRG"},{"y":"WRNW.MI","c":"Tematici","t":"WRNW"},
    {"y":"WSLV.MI","c":"Tematici","t":"WSLV"},{"y":"WTAI.MI","c":"Tematici","t":"WTAI"},
    {"y":"WTEC.MI","c":"Settoriali SPDR WORLD","t":"WTEC"},{"y":"WTEL.MI","c":"Settoriali SPDR WORLD","t":"WTEL"},
    {"y":"WTI.MI","c":"Materie","t":"WTI"},{"y":"WTID.MI","c":"Materie","t":"WTID"},
    {"y":"WTRE.MI","c":"Tematici","t":"WTRE"},{"y":"WUTI.MI","c":"Settoriali SPDR WORLD","t":"WUTI"},
    {"y":"XAIX.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"XAIX"},{"y":"XCHA.MI","c":"Paesi","t":"XCHA"},
    {"y":"XCS5.MI","c":"Paesi","t":"XCS5"},{"y":"XCTE.MI","c":"Tematici","t":"XCTE"},
    {"y":"XDAX.MI","c":"Paesi","t":"XDAX"},{"y":"XDBC.MI","c":"Materie","t":"XDBC"},
    {"y":"XDEE.MI","c":"NEW AREA, Paesi","t":"XDEE"},{"y":"XDER.MI","c":"Tematici","t":"XDER"},
    {"y":"XDEV.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"XDEV"},{"y":"XDG3.MI","c":"Tematici","t":"XDG3"},
    {"y":"XDG6.MI","c":"Tematici","t":"XDG6"},{"y":"XDG7.MI","c":"Tematici","t":"XDG7"},
    {"y":"XDGI.MI","c":"Tematici","t":"XDGI"},{"y":"XDRE.MI","c":"Settoriali","t":"XDRE"},
    {"y":"XEON.MI","c":"Liquidità","t":"XEON"},{"y":"XFNT.MI","c":"Tematici","t":"XFNT"},
    {"y":"XFVT.MI","c":"Paesi","t":"XFVT"},{"y":"XG11.MI","c":"Tematici","t":"XG11"},
    {"y":"XG12.MI","c":"Tematici","t":"XG12"},{"y":"XGEN.MI","c":"Tematici","t":"XGEN"},
    {"y":"XIFE.MI","c":"Settoriali","t":"XIFE"},{"y":"XLBS.MI","c":"Settoriali","t":"XLBS"},
    {"y":"XLCS.MI","c":"Settoriali","t":"XLCS"},{"y":"XLES.MI","c":"Settoriali","t":"XLES"},
    {"y":"XLFS.MI","c":"Settoriali","t":"XLFS"},{"y":"XLIS.MI","c":"Settoriali","t":"XLIS"},
    {"y":"XLKS.MI","c":"Settoriali","t":"XLKS"},{"y":"XLPE.MI","c":"Tematici","t":"XLPE"},
    {"y":"XLPS.MI","c":"Settoriali","t":"XLPS"},{"y":"XLUS.MI","c":"Settoriali","t":"XLUS"},
    {"y":"XLVS.MI","c":"Settoriali","t":"XLVS"},{"y":"XLYS.MI","c":"Settoriali","t":"XLYS"},
    {"y":"XMME.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"XMME"},{"y":"XMOV.MI","c":"Tematici","t":"XMOV"},
    {"y":"XNGI.MI","c":"Tematici","t":"XNGI"},{"y":"XNNV.MI","c":"Tematici","t":"XNNV"},
    {"y":"XRES.MI","c":"Tematici","t":"XRES"},{"y":"XS8R.MI","c":"Tematici","t":"XS8R"},
    {"y":"XSFR.MI","c":"Paesi","t":"XSFR"},{"y":"XSGI.MI","c":"Tematici","t":"XSGI"},
    {"y":"XSMI.MI","c":"Paesi","t":"XSMI"},{"y":"XSX6.MI","c":"ADVICE_MONEYFARM_OPERATIVE","t":"XSX6"},
    {"y":"XUTC.MI","c":"Settoriali","t":"XUTC"},{"y":"XWTS.MI","c":"Settoriali","t":"XWTS"},
    {"y":"ZINC.MI","c":"Materie","t":"ZINC"},{"y":"X13E.MI","c":"Liquidità","t":"X13E"},
    {"y":"EM13.MI","c":"Liquidità","t":"EM13"},{"y":"ERNE.MI","c":"Liquidità","t":"ERNE"},
    {"y":"INFR.MI","c":"REAL ESTATE","t":"INFR"},{"y":"SXLE.MI","c":"Settoriali SPDR USA","t":"SXLE"},
    {"y":"MGIN.MI","c":"Settoriali SPDR USA","t":"MGIN"},{"y":"STWX.MI","c":"Settoriali SPDR EURO","t":"STWX"},
    {"y":"STZX.MI","c":"Settoriali SPDR EURO","t":"STZX"},{"y":"SWRD.MI","c":"BENCHMARK SETT SPDR WORLD","t":"SWRD"},
    {"y":"600X.MI","c":"BENCHMARK SETT SPDR EURO","t":"600X"},
    {"y":"ADS.DE","c":"EUROGROW ISHARES","t":"ADS"},{"y":"ADYEN.AS","c":"EUROGROW ISHARES","t":"ADYEN"},
    {"y":"AI.PA","c":"EUROGROW ISHARES","t":"AI"},{"y":"AIR.PA","c":"EUROGROW ISHARES","t":"AIR"},
    {"y":"AM.PA","c":"EUROGROW ISHARES","t":"AM"},{"y":"ARGX","c":"EUROGROW ISHARES","t":"ARGX"},
    {"y":"ASML.SW","c":"EUROGROW ISHARES","t":"ASML"},{"y":"BEI.DE","c":"EUROGROW ISHARES","t":"BEI"},
    {"y":"CBK.DE","c":"EUROGROW ISHARES","t":"CBK"},{"y":"DB1.DE","c":"EUROGROW ISHARES","t":"DB1"},
    {"y":"DIM.PA","c":"EUROGROW ISHARES","t":"DIM"},{"y":"DSY.PA","c":"EUROGROW ISHARES","t":"DSY"},
    {"y":"DTE.DE","c":"EUROGROW ISHARES","t":"DTE"},{"y":"EL.PA","c":"EUROGROW ISHARES","t":"EL"},
    {"y":"ELE.MC","c":"EUROGROW ISHARES","t":"ELE"},{"y":"ENR.DE","c":"EUROGROW ISHARES","t":"ENR"},
    {"y":"FER.MC","c":"EUROGROW ISHARES","t":"FER"},{"y":"HO.PA","c":"EUROGROW ISHARES","t":"HO"},
    {"y":"IFX.DE","c":"EUROGROW ISHARES","t":"IFX"},{"y":"KNEBV.HE","c":"EUROGROW ISHARES","t":"KNEBV"},
    {"y":"LDO.MI","c":"EUROGROW ISHARES","t":"LDO"},{"y":"LR.PA","c":"EUROGROW ISHARES","t":"LR"},
    {"y":"MC.PA","c":"EUROGROW ISHARES","t":"MC"},{"y":"NOKIA.HE","c":"EUROGROW ISHARES","t":"NOKIA"},
    {"y":"OR.PA","c":"EUROGROW ISHARES","t":"OR"},{"y":"PRX.AS","c":"EUROGROW ISHARES","t":"PRX"},
    {"y":"PRY.MI","c":"EUROGROW ISHARES","t":"PRY"},{"y":"RACE.MI","c":"EUROGROW ISHARES","t":"RACE"},
    {"y":"RHM.DE","c":"EUROGROW ISHARES","t":"RHM"},{"y":"RMS.PA","c":"EUROGROW ISHARES","t":"RMS"},
    {"y":"SAF.PA","c":"EUROGROW ISHARES","t":"SAF"},{"y":"SAP.DE","c":"EUROGROW ISHARES","t":"SAP"},
    {"y":"SHL.DE","c":"EUROGROW ISHARES","t":"SHL"},{"y":"SIE.DE","c":"EUROGROW ISHARES","t":"SIE"},
    {"y":"SU.PA","c":"EUROGROW ISHARES","t":"SU"},{"y":"UCG.MI","c":"EUROGROW ISHARES","t":"UCG"},
    {"y":"WKL.VI","c":"EUROGROW ISHARES","t":"WKL"},
    {"y":"EEM","c":"top4 logical usa","t":"EEM"},{"y":"QQQ","c":"top4 logical usa","t":"QQQ"},
    {"y":"SPY","c":"top4 logical usa","t":"SPY"},{"y":"EWZ","c":"top4 logical usa","t":"EWZ"},
    {"y":"EWG","c":"top4 logical usa","t":"EWG"},{"y":"EWJ","c":"top4 logical usa","t":"EWJ"},
    {"y":"EWT","c":"top4 logical usa","t":"EWT"},{"y":"EWY","c":"top4 logical usa","t":"EWY"},
]

# ── INDICATORI ──────────────────────────────────────────────
def safe_float(v):
    """Converte a float, restituisce None se NaN/None/inf"""
    try:
        f = float(v)
        if math.isnan(f) or math.isinf(f):
            return None
        return f
    except:
        return None

def safe_val(v, default=0.0):
    r = safe_float(v)
    return r if r is not None else default

def ema(series, n):
    k = 2/(n+1)
    out = [None]*len(series)
    started = False
    prev = None
    for i, v in enumerate(series):
        if v is None:
            continue
        if not started:
            out[i] = v
            prev = v
            started = True
        else:
            out[i] = v*k + prev*(1-k)
            prev = out[i]
    return out

def sma(series, n):
    out = [None]*len(series)
    for i in range(len(series)):
        if i < n-1:
            continue
        sl = series[i-n+1:i+1]
        if any(v is None for v in sl):
            continue
        out[i] = sum(sl)/n
    return out

def calc_kama(cs, n=10, fast=2, slow=30):
    fsc = 2/(fast+1)
    ssc = 2/(slow+1)
    out = [None]*len(cs)
    prev = None
    for i in range(len(cs)):
        if cs[i] is None:
            continue
        if prev is None:
            out[i] = cs[i]
            prev = cs[i]
            continue
        if i < n:
            out[i] = prev
            continue
        direction = abs(cs[i] - cs[i-n])
        volatility = sum(abs(cs[j]-cs[j-1]) for j in range(i-n+1, i+1) if cs[j] is not None and cs[j-1] is not None)
        er = direction/volatility if volatility > 0 else 0
        sc = (er*(fsc-ssc)+ssc)**2
        out[i] = prev + sc*(cs[i]-prev)
        prev = out[i]
    return out

def calc_rsi(cs, n=14):
    out = [None]*len(cs)
    if len(cs) < n+1:
        return out
    gains, losses = 0, 0
    for i in range(1, n+1):
        d = cs[i]-cs[i-1]
        if d > 0: gains += d
        else: losses -= d
    ag, al = gains/n, losses/n
    out[n] = 100 if al==0 else 100-100/(1+ag/al)
    for i in range(n+1, len(cs)):
        d = cs[i]-cs[i-1]
        ag = (ag*(n-1)+(d if d>0 else 0))/n
        al = (al*(n-1)+(-d if d<0 else 0))/n
        out[i] = 100 if al==0 else 100-100/(1+ag/al)
    return out

def calc_er(cs, n=10):
    out = [None]*len(cs)
    for i in range(n, len(cs)):
        direction = abs(cs[i]-cs[i-n])
        volatility = sum(abs(cs[j]-cs[j-1]) for j in range(i-n+1, i+1))
        out[i] = direction/volatility if volatility > 0 else 0
    return out

def calc_trendycator(cs):
    ef = ema(cs, 21)
    el = ema(cs, 55)
    out = [0]*len(cs)
    for i in range(1, len(cs)):
        if ef[i] is None or el[i] is None or ef[i-1] is None:
            continue
        if ef[i] > el[i] and ef[i] > ef[i-1]:
            out[i] = 1
        elif ef[i] < el[i] and ef[i] < ef[i-1]:
            out[i] = -1
    return out

def calc_baffetti(ao):
    n = len(ao)-1
    count = 0
    for i in range(n, 0, -1):
        if ao[i] is None or ao[i-1] is None:
            break
        if ao[i] > ao[i-1]:
            count += 1
        else:
            break
    return count

def find_crossover_date(cs, kama, dates):
    n = len(cs)-1
    for i in range(n, 0, -1):
        if kama[i] is None or kama[i-1] is None:
            continue
        if cs[i] > kama[i] and cs[i-1] <= kama[i-1]:
            return dates[i].strftime('%d/%m/%Y')
    return '—'

def calc_perf(cs, days):
    n = len(cs)-1
    if n < days:
        return 0
    prev = cs[n-days]
    if not prev:
        return 0
    return (cs[n]-prev)/prev*100

# ── PROCESSA UN TICKER ───────────────────────────────────────
def process_ticker(info):
    try:
        tk = yf.Ticker(info['y'])
        hist = tk.history(period='1y', interval='1d', auto_adjust=True)
        if hist is None or len(hist) < 60:
            return {'ticker': info['y'], 'display': info['t'], 'categoria': info['c'],
                    'nome': info['t'], 'error': 'Dati insufficienti'}

        cs = [safe_float(v) for v in hist['Close'].tolist()]
        hs = [safe_float(v) for v in hist['High'].tolist()]
        ls = [safe_float(v) for v in hist['Low'].tolist()]
        valid = [v for v in cs if v is not None]
        if len(valid) < 60:
            return {'ticker': info['y'], 'display': info['t'], 'categoria': info['c'],
                    'nome': info['t'], 'error': 'Dati insufficienti (NaN)'}
        dates = list(hist.index)
        n = len(cs)-1

        kama = calc_kama(cs)
        e7 = ema(cs, 7)
        e34 = ema(cs, 34)
        ao = [e7[i]-e34[i] if e7[i] is not None and e34[i] is not None else None for i in range(len(cs))]
        rsi_vals = calc_rsi(cs, 14)
        er_vals = calc_er(cs, 10)
        mm20 = sma(cs, 20)
        mm50 = sma(cs, 50)
        mm200 = sma(cs, 200)
        tc = calc_trendycator(cs)

        lc = cs[n]
        lk = kama[n]
        lr = safe_val(rsi_vals[n], 50.0)
        ler = safe_val(er_vals[n], 0.0)
        lao = safe_val(ao[n], 0.0)
        lmm20 = mm20[n]
        lmm50 = mm50[n]
        ltc = tc[n]

        stato = 'VERDE' if ltc == 1 else 'ROSSO' if ltc == -1 else 'GRIGIO'
        p_above_kama = bool(lk is not None and lc > lk)
        er_ok = bool(ler >= 0.5)
        baff_count = calc_baffetti(ao)
        baf3 = bool(baff_count >= 3)
        mm_align = bool(lmm20 is not None and lmm50 is not None and lc > lmm20 and lmm20 > lmm50)
        ao_positive = bool(lao > 0)
        entry_date = find_crossover_date(cs, kama, dates)
        perf_sett = round(calc_perf(cs, 5), 2)
        perf_mese = round(calc_perf(cs, 22), 2)

        # Score
        er_score = ler * 30
        baff_score = min(baff_count, 10) * 5
        pk_pct = abs((lc-lk)/lk*100) if lk else 0
        pk_score = min(pk_pct, 5) * 3
        sett_score = min(max(perf_sett, -10), 5) * 4
        mese_score = min(max(perf_mese, -20), 10) * 2
        mm_bonus = 10 if mm_align else 0
        ao_bonus = 5 if ao_positive else 0

        # CrossDays
        cross_days = 999
        for i in range(n, 0, -1):
            if kama[i] is None or kama[i-1] is None:
                continue
            if cs[i] > kama[i] and cs[i-1] <= kama[i-1]:
                cross_days = n - i
                break
        cross_bonus = 20 if cross_days <= 3 else 12 if cross_days <= 10 else 5 if cross_days <= 20 else 0

        score = er_score + baff_score + pk_score + sett_score + mese_score + mm_bonus + ao_bonus + cross_bonus
        if stato == 'ROSSO':
            score *= 0.6
        if not math.isfinite(score): score = 0.0
        score = max(0, round(score * 10) / 10)

        # Segnale
        tipo = ''
        if stato == 'VERDE' and p_above_kama and er_ok and baf3 and mm_align:
            tipo = '🟢 LONG'
        elif p_above_kama and baf3 and stato in ('VERDE', 'GRIGIO'):
            tipo = '🔵 EARLY'
        elif p_above_kama and baff_count >= 1 and stato in ('VERDE', 'GRIGIO'):
            tipo = '🟡 WATCH'
        elif stato == 'ROSSO' and cross_days <= 3 and baf3:
            tipo = '⚪ ROSSO+'

        uscita = ''
        if stato == 'ROSSO':
            uscita = '⛔ STOP'
        elif not p_above_kama:
            uscita = '🔴 USCITA'
        elif stato == 'GRIGIO' or lao <= 0:
            uscita = '🟡 ATTENZIONE'

        nome = info['t']
        try:
            info_data = tk.info
            nome = info_data.get('longName') or info_data.get('shortName') or info['t']
        except:
            pass

        # Segnale compatibile command center
        signal = 'BUY' if tipo in ('🟢 LONG', '🔵 EARLY') else 'HOLD' if tipo == '🟡 WATCH' else 'SELL' if uscita in ('⛔ STOP', '🔴 USCITA') else ''

        return {
            'ticker': info['y'], 'display': info['t'], 'nome': nome,
            'categoria': info['c'],
            'prezzo': round(lc, 4), 'kama': round(lk, 4) if lk else None,
            'er': round(ler, 4), 'ao': round(lao, 4), 'rsi': round(lr, 2),
            'pAboveKama': p_above_kama, 'erOk': er_ok,
            'baf3': baf3, 'baffCount': baff_count,
            'mmAlign': mm_align, 'aoPositive': ao_positive,
            'crossDays': cross_days, 'entryDate': entry_date,
            'pkPct': round(pk_pct, 3),
            'perfSett': perf_sett, 'perfMese': perf_mese,
            'stato': stato, 'score': score,
            'tipo': tipo, 'uscita': uscita,
            'signal': signal,
            'error': None
        }
    except Exception as e:
        return {
            'ticker': info['y'], 'display': info['t'], 'categoria': info['c'],
            'nome': info['t'], 'error': str(e)[:80],
            'score': 0, 'tipo': '', 'uscita': '', 'signal': '',
            'stato': '—', 'prezzo': None
        }

# ── MAIN ────────────────────────────────────────────────────
def main():
    print(f"[RAPTOR Ranking] Start — {len(TICKERS)} ticker")
    results = []
    errors = 0

    for i, info in enumerate(TICKERS):
        r = process_ticker(info)
        results.append(r)
        if r.get('error'):
            errors += 1
            print(f"  ✗ {info['y']}: {r['error']}")
        else:
            if (i+1) % 50 == 0:
                print(f"  ✓ {i+1}/{len(TICKERS)} — {errors} errori finora")

    # Sort by score desc
    results.sort(key=lambda x: x.get('score', 0), reverse=True)
    for i, r in enumerate(results):
        r['rank'] = i+1

    now = datetime.now(timezone.utc)
    out = {
        'meta': {
            'updated': now.isoformat(),
            'updated_it': now.strftime('%d/%m/%Y %H:%M'),
            'total': len(results),
            'errors': errors,
            'long': len([r for r in results if r.get('tipo')=='🟢 LONG']),
            'early': len([r for r in results if r.get('tipo')=='🔵 EARLY']),
            'watch': len([r for r in results if r.get('tipo')=='🟡 WATCH']),
        },
        'data': results
    }

    os.makedirs('data', exist_ok=True)
    with open('data/ranking.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))

    print(f"[RAPTOR Ranking] Done — {len(results)} ticker, {errors} errori")
    print(f"  LONG: {out['meta']['long']} | EARLY: {out['meta']['early']} | WATCH: {out['meta']['watch']}")

if __name__ == '__main__':
    main()
