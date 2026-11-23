char __fastcall sub_140DC4DB0(__int64 a1, char a2, char a3)
{
  __int64 v6; // rax
  __int64 v7; // rcx
  unsigned __int8 v8; // al
  unsigned int v9; // ecx
  int v10; // edi
  unsigned __int64 v11; // rdi
  __int64 v12; // rbp
  __int64 v13; // rcx
  unsigned __int8 v14; // al
  unsigned __int8 v15; // cl
  unsigned int v16; // edx
  char result; // al
  int v18; // ebp
  unsigned __int64 v19; // rdx
  __int64 v20; // rbp
  __int64 *v21; // rax
  __int64 v22; // rcx
  unsigned __int64 v23; // rax
  __int64 v24; // rcx
  __int64 v25; // rcx
  __int64 v26; // rcx
  __int64 v27; // rcx
  __int64 v28; // rcx
  __int64 v29; // rcx
  __int64 v30; // rcx
  __int64 v31; // rcx
  __int64 v32; // rcx
  __int64 v33; // rcx
  __int64 v34; // rcx
  __int64 v35; // rcx
  __int64 v36; // rcx
  __int64 v37; // rcx
  __int64 v38; // rcx
  __int64 v39; // rcx
  __int64 v40; // rcx
  __int64 v41; // rcx
  __int64 v42; // rcx
  __int64 v43; // rcx
  __int64 v44; // rcx
  __int64 v45; // rcx
  __int64 v46; // rcx
  __int64 v47; // rcx
  __int64 v48; // rcx
  __int64 v49; // rcx
  __int64 v50; // rcx
  __int64 v51; // rcx
  unsigned int v52; // eax
  unsigned __int16 v53; // cx
  __int64 v54; // rcx
  _QWORD *v55; // rdi
  __int64 v56; // rcx
  __int64 v57; // rdx
  __int64 v58; // rcx
  _QWORD *v59; // rdi
  __int64 v60; // rcx
  __int64 v61; // rcx
  __int64 v62; // rcx
  __int64 v63; // rcx
  __int64 v64; // rcx
  __int64 v65; // rcx
  __int64 v66; // rcx
  __int64 v67; // rcx
  __int64 v68; // rcx
  __int64 v69; // rcx
  __int64 v70; // rcx
  __int64 v71; // rcx
  __int64 v72; // rcx
  __int64 v73; // rcx
  __int64 v74; // rcx
  __int64 v75; // rcx
  __int64 v76; // rcx
  __int64 v77; // rcx
  __int64 v78; // r8
  int v79; // [rsp+28h] [rbp-40h] BYREF
  _QWORD v80[7]; // [rsp+30h] [rbp-38h] BYREF

  v6 = *(int *)(*(_QWORD *)(a1 + 8) + 8LL);
  v7 = *(_QWORD *)(v6 + a1 + 168);
  if ( v7 != 0 || (v21 = *(__int64 **)(a1 + v6 + 176)) != nullptr && (v7 = *v21, *v21 != 0) )
  {
    if ( (v8 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v7 + 80LL))(v7),
          (unsigned __int8)(v9 = v8 & 0xFE) <= 0x18u)
      && (v10 = 16777296, _bittest(&v10, v9))
      || v9 == 70
      || v9 == 84
      || (unsigned int)(v11 = (unsigned int)v8 - 8) <= 0x3B && (v12 = 0xC00000000000003LL, _bittest64(&v12, v11))
      || (v8 & 0xF6) == 0x26
      || (v8 & 0xFE) == 0x44
      || v9 == 28 )
    {
      v13 = *(_QWORD *)(*(int *)(*(_QWORD *)(a1 + 8) + 8LL) + a1 + 168);
      if ( v13 == 0 )
        return 0;
      v14 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v13 + 104LL))(v13);
      if ( v14 == 0 )
        return 0;
      v15 = v14;
      v16 = v14 & 0xFE;
      result = 0;
      if ( (unsigned __int8)v16 <= 0x18u )
      {
        v18 = 16777296;
        if ( _bittest(&v18, v16) )
          return result;
      }
      if ( v16 == 70 || v16 == 84 )
        return result;
      v19 = (unsigned int)v15 - 8;
      if ( (unsigned int)v19 <= 0x3B )
      {
        v20 = 0xC00000000000003LL;
        if ( _bittest64(&v20, v19) )
          return 0;
      }
      if ( (v15 & 0xF6) == 0x26 )
        return 0;
      v23 = (unsigned int)v15 - 28;
      if ( (unsigned int)v23 <= 0x29 )
      {
        v24 = 0x30000000003LL;
        if ( _bittest64(&v24, v23) )
          return 0;
      }
    }
  }
  result = 0;
  switch ( a2 )
  {
    case 0:
      v22 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v22 + 528LL))(v22) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      result = *(_BYTE *)(a1 + 51);
      goto LABEL_105;
    case 1:
      v25 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v25 + 528LL))(v25) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      result = *(_BYTE *)(a1 + 65);
      goto LABEL_105;
    case 2:
      v26 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v26 + 528LL))(v26) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      result = *(_BYTE *)(a1 + 66);
      goto LABEL_105;
    case 3:
      v27 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v27 + 528LL))(v27) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      return *(_BYTE *)(a1 + 36);
    case 4:
      v28 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v28 + 528LL))(v28) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      result = *(_BYTE *)(a1 + 54);
      goto LABEL_105;
    case 5:
      v29 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v29 + 528LL))(v29) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      result = *(_BYTE *)(a1 + 58);
      goto LABEL_105;
    case 6:
      v30 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v30 + 528LL))(v30) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      result = *(_BYTE *)(a1 + 59);
      goto LABEL_105;
    case 7:
      v31 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v31 + 528LL))(v31) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      result = *(_BYTE *)(a1 + 60);
      goto LABEL_105;
    case 8:
      v32 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v32 + 528LL))(v32) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      result = *(_BYTE *)(a1 + 61);
      goto LABEL_105;
    case 9:
      v33 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v33 + 528LL))(v33) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      result = *(_BYTE *)(a1 + 62);
      goto LABEL_105;
    case 10:
      v34 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v34 + 528LL))(v34) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      result = *(_BYTE *)(a1 + 63);
      goto LABEL_105;
    case 11:
      v35 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v35 + 528LL))(v35) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      result = *(_BYTE *)(a1 + 75);
      goto LABEL_105;
    case 12:
      v36 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v36 + 528LL))(v36) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      v37 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v37 + 528LL))(v37) != 0 )
        return 0;
      result = *(_BYTE *)(a1 + 57);
      goto LABEL_105;
    case 13:
      v38 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v38 + 528LL))(v38) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      return *(_BYTE *)(*(int *)(*(_QWORD *)(a1 + 8) + 8LL) + a1 + 88);
    case 14:
      v39 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v39 + 528LL))(v39) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      result = *(_BYTE *)(a1 + 37);
      goto LABEL_105;
    case 15:
      v40 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v40 + 528LL))(v40) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      result = *(_BYTE *)(a1 + 52);
      goto LABEL_105;
    case 16:
      v41 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v41 + 528LL))(v41) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      result = *(_BYTE *)(a1 + 53);
      goto LABEL_105;
    case 17:
      v42 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v42 + 528LL))(v42) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      return *(_BYTE *)(a1 + 28);
    case 18:
      v43 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v43 + 528LL))(v43) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      result = *(_BYTE *)(a1 + 55);
      goto LABEL_105;
    case 19:
      v44 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v44 + 528LL))(v44) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      v45 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v45 + 528LL))(v45) != 0 )
        return 0;
      result = *(_BYTE *)(a1 + 56);
      goto LABEL_105;
    case 20:
      v46 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v46 + 528LL))(v46) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      result = *(_BYTE *)(a1 + 68);
      goto LABEL_105;
    case 21:
      v47 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v47 + 528LL))(v47) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      result = *(_BYTE *)(a1 + 74);
      goto LABEL_105;
    case 22:
      v48 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v48 + 528LL))(v48) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      v49 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v49 + 528LL))(v49) != 0 )
        return 0;
      result = *(_BYTE *)(a1 + 71);
      goto LABEL_105;
    case 23:
      v50 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v50 + 528LL))(v50) != 0
        && (unsigned __int8)sub_1400015B0() != 0 )
      {
        return 0;
      }
      v51 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v51 + 528LL))(v51) != 0 )
        return 0;
      result = *(_BYTE *)(a1 + 73);
LABEL_105:
      if ( a3 != 0 )
      {
        v52 = ((unsigned int)(26215 * result + 52430) >> 31) + ((26215 * result + 52430) >> 17);
        v53 = 1;
        if ( (__int16)v52 >= 2 )
          v53 = v52;
        result = 20;
        if ( v53 < 0x14u )
          return v53;
      }
      return result;
    case 24:
      v54 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v54 + 528LL))(v54) == 0 )
        return (**(__int64 (__fastcall ***)(__int64))a1)(a1);
      v55 = *(_QWORD **)(*(int *)(*(_QWORD *)(a1 + 8) + 8LL) + a1 + 168);
      if ( v55 != nullptr && (*(unsigned __int8 (__fastcall **)(_QWORD *))(*v55 + 80LL))(v55) >= 2u )
      {
        v56 = v55[2];
        if ( v56 != 0 )
        {
          v57 = *(_QWORD *)(a1 + 8);
LABEL_154:
          memset(v80, 240, 8);
          sub_1411AF6C0(v56, *(unsigned int *)(*(int *)(v57 + 4) + a1 + 20), v80);
          v79 = 536;
          LOBYTE(v78) = 1;
          return sub_141332360(v80, &v79, v78);
        }
      }
      v57 = *(_QWORD *)(a1 + 8);
      v76 = *(_QWORD *)(*(int *)(v57 + 8) + a1 + 176);
      result = 3;
      if ( v76 != 0 )
      {
        v77 = *(_QWORD *)(v76 + 16);
        if ( v77 != 0 )
        {
          v56 = *(_QWORD *)(v77 + 16);
          if ( v56 != 0 )
            goto LABEL_154;
        }
      }
      break;
    case 25:
      return *(_BYTE *)(a1 + 27);
    case 26:
      return sub_140DC19E0(a1, 0);
    case 27:
      v58 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v58 + 528LL))(v58) == 0 )
        return *(_BYTE *)(a1 + 24);
      v59 = *(_QWORD **)(*(int *)(*(_QWORD *)(a1 + 8) + 8LL) + a1 + 168);
      if ( v59 != nullptr && (*(unsigned __int8 (__fastcall **)(_QWORD *))(*v59 + 80LL))(v59) >= 2u && v59[2] != 0 )
        return sub_1411AFAF0();
      v60 = *(_QWORD *)(*(int *)(*(_QWORD *)(a1 + 8) + 8LL) + a1 + 176);
      result = 10;
      if ( v60 != 0 )
      {
        v61 = *(_QWORD *)(v60 + 16);
        if ( v61 != 0 && *(_QWORD *)(v61 + 16) != 0 )
          return sub_1411AFAF0();
      }
      return result;
    case 28:
      return *(_BYTE *)(a1 + 34);
    case 29:
      return *(_BYTE *)(a1 + 31);
    case 33:
      return *(_BYTE *)(a1 + 229);
    case 34:
      return *(_BYTE *)(a1 + 230);
    case 35:
      return *(_BYTE *)(a1 + 231);
    case 36:
      return *(_BYTE *)(a1 + 232);
    case 37:
      return *(_BYTE *)(a1 + 233);
    case 38:
      return *(_BYTE *)(a1 + 234);
    case 39:
      return *(_BYTE *)(a1 + 235);
    case 40:
      v62 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v62 + 528LL))(v62) == 0 )
        return 0;
      v63 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      return *(_BYTE *)((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v63 + 1760LL))(v63) + 1082);
    case 41:
      v64 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v64 + 528LL))(v64) == 0 )
        return 0;
      v65 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      return *(_BYTE *)((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v65 + 1760LL))(v65) + 1083);
    case 42:
      v66 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v66 + 528LL))(v66) == 0 )
        return 0;
      v67 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      return *(_BYTE *)((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v67 + 1760LL))(v67) + 1084);
    case 43:
      v68 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v68 + 528LL))(v68) == 0 )
        return 0;
      v69 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      return *(_BYTE *)((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v69 + 1760LL))(v69) + 1085);
    case 44:
      v70 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v70 + 528LL))(v70) == 0 )
        return 0;
      v71 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      return *(_BYTE *)((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v71 + 1760LL))(v71) + 1086);
    case 45:
      v72 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v72 + 528LL))(v72) == 0 )
        return 0;
      v73 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      return *(_BYTE *)((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v73 + 1760LL))(v73) + 1087);
    case 46:
      v74 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v74 + 528LL))(v74) == 0 )
        return 0;
      v75 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
      return *(_BYTE *)((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v75 + 1760LL))(v75) + 1088);
    default:
      return result;
  }
  return result;
}
