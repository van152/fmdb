char __fastcall sub_14118E6D0(__int64 a1, int a2, __int64 *a3)
{
  __int64 v4; // rcx
  int v5; // eax
  int v6; // ecx
  int v7; // edi
  __int64 v8; // rax
  unsigned __int64 v9; // rax
  __int64 v10; // rcx
  int v11; // edi
  unsigned __int64 v12; // rax
  __int64 v13; // rcx
  unsigned __int64 *v14; // rcx
  __int64 v15; // rdx
  int v16; // edi
  unsigned __int64 v17; // rax
  __int64 v18; // rcx
  int v19; // edi
  unsigned __int64 v20; // rax
  __int64 v21; // rcx
  int v22; // edi
  unsigned __int64 v23; // rax
  __int64 v24; // rcx
  int v25; // edi
  unsigned __int64 v26; // rax
  __int64 v27; // rcx
  int v28; // edi
  unsigned __int64 v29; // rax
  __int64 v30; // rcx
  int v31; // edi
  unsigned __int64 v32; // rax
  __int64 v33; // rcx
  __int64 *v34; // rdi
  __int64 v35; // rax
  __int64 v36; // rcx
  unsigned __int64 v37; // rax
  __int64 v38; // rcx
  __int64 v39; // rcx
  unsigned __int64 *v40; // rdi
  char v41; // bl
  unsigned __int64 v42; // rax
  __int64 v43; // rcx
  int v44; // edi
  unsigned __int64 v45; // rax
  __int64 v46; // rcx
  int v47; // edi
  unsigned __int64 v48; // rax
  __int64 v49; // rcx
  char v50; // bl
  unsigned __int64 v51; // rax
  __int64 v52; // rcx
  int v53; // edi
  unsigned __int64 v54; // rax
  __int64 v55; // rcx
  __int64 *v56; // rdi
  __int64 v57; // rax
  __int64 v58; // rcx
  unsigned __int64 v59; // rax
  __int64 v60; // rcx
  int v62; // edi
  unsigned __int64 v63; // rax
  __int64 v64; // rcx
  __int64 *v65; // rdi
  __int64 v66; // rax
  __int64 v67; // rcx
  unsigned __int64 v68; // rax
  __int64 v69; // rcx
  int v70; // edi
  unsigned __int64 v71; // rax
  __int64 v72; // rcx
  unsigned __int64 v73; // [rsp+20h] [rbp-10h] BYREF
  _QWORD v74[5]; // [rsp+28h] [rbp-8h] BYREF

  v74[1] = -2;
  if ( a2 <= 1095250530 )
  {
    if ( a2 > 1093886310 )
    {
      switch ( a2 )
      {
        case 1095250275:
          v4 = *(_QWORD *)(a1 + 40);
          if ( v4 != 0 )
          {
LABEL_28:
            v5 = *(_DWORD *)(v4 + 12);
            v6 = *(_DWORD *)(v4 + 16);
            if ( v6 == 0 )
              v6 = v5;
          }
          else
          {
LABEL_10:
            v5 = -1;
            v6 = -1;
          }
          v73 = __PAIR64__(v6, v5);
          v14 = &v73;
          v15 = 1315856756;
          goto LABEL_113;
        case 1095250276:
        case 1095250277:
        case 1095250278:
        case 1095250279:
        case 1095250280:
        case 1095250282:
        case 1095250283:
        case 1095250284:
        case 1095250285:
        case 1095250287:
        case 1095250289:
        case 1095250290:
        case 1095250291:
          return sub_140FE3F20((_DWORD *)a1, a2, a3);
        case 1095250281:
          v62 = *(unsigned __int16 *)(a1 + 142);
          if ( *(_WORD *)(a1 + 142) == 0 )
            goto LABEL_118;
          v8 = sub_14083D4F0(a1) + 40;
          LODWORD(v74[0]) = v62;
          v73 = v8;
          if ( &v73 != (unsigned __int64 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v63 = v73;
            v64 = v74[0];
            a3[1] = v74[0];
            *a3 = v63;
            v8 = sub_14083D4F0(v64) + 8;
            v74[0] = 0;
            v73 = v8;
          }
          goto LABEL_72;
        case 1095250286:
          v65 = (__int64 *)(a1 + 80);
          v66 = sub_14083D4F0(a1);
          v74[0] = 0;
          if ( v74 != v65 )
          {
            v67 = *v65;
            if ( *v65 != 0 )
              _InterlockedIncrement((volatile signed __int32 *)(v67 - 4));
            v74[0] = v67;
          }
          v8 = v66 + 136;
          v73 = v8;
          if ( &v73 != (unsigned __int64 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v68 = v73;
            v69 = v74[0];
            a3[1] = v74[0];
            *a3 = v68;
            v8 = sub_14083D4F0(v69) + 8;
            v74[0] = 0;
            v73 = v8;
          }
          goto LABEL_72;
        case 1095250288:
          v39 = *(_QWORD *)(a1 + 32);
LABEL_110:
          sub_140FE7F20(v39, a3);
          return 1;
        case 1095250292:
          v40 = (unsigned __int64 *)(a1 + 104);
LABEL_112:
          v14 = v40;
          v15 = 1416914273;
LABEL_113:
          sub_140FE72B0(v14, v15, a3);
          return 1;
        default:
          if ( a2 == 1093886311 )
          {
            v70 = *(unsigned __int8 *)(a1 + 154);
            if ( (char)v70 <= 0 )
              goto LABEL_118;
            v8 = sub_14083D4F0(a1) + 40;
            LODWORD(v74[0]) = v70;
            v73 = v8;
            if ( &v73 != (unsigned __int64 *)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v71 = v73;
              v72 = v74[0];
              a3[1] = v74[0];
              *a3 = v71;
              v8 = sub_14083D4F0(v72) + 8;
              v74[0] = 0;
              v73 = v8;
            }
            goto LABEL_72;
          }
          if ( a2 != 1093888306 )
            return sub_140FE3F20((_DWORD *)a1, a2, a3);
          v22 = *(unsigned __int16 *)(a1 + 152);
          if ( *(_WORD *)(a1 + 152) != 0 )
          {
            v8 = sub_14083D4F0(a1) + 40;
            LODWORD(v74[0]) = v22;
            v73 = v8;
            if ( &v73 != (unsigned __int64 *)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v23 = v73;
              v24 = v74[0];
              a3[1] = v74[0];
              *a3 = v23;
              v8 = sub_14083D4F0(v24) + 8;
              v74[0] = 0;
              v73 = v8;
            }
            goto LABEL_72;
          }
          break;
      }
      goto LABEL_118;
    }
    if ( a2 > 1093820774 )
    {
      if ( a2 == 1093820775 )
      {
        v28 = *(unsigned __int8 *)(a1 + 156);
        if ( (char)v28 > 0 )
        {
          v8 = sub_14083D4F0(a1) + 40;
          LODWORD(v74[0]) = v28;
          v73 = v8;
          if ( &v73 != (unsigned __int64 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v29 = v73;
            v30 = v74[0];
            a3[1] = v74[0];
            *a3 = v29;
            v8 = sub_14083D4F0(v30) + 8;
            v74[0] = 0;
            v73 = v8;
          }
          goto LABEL_72;
        }
        goto LABEL_118;
      }
      if ( a2 == 1093822770 )
      {
        v19 = *(unsigned __int16 *)(a1 + 148);
        if ( *(_WORD *)(a1 + 148) != 0 )
        {
          v8 = sub_14083D4F0(a1) + 40;
          LODWORD(v74[0]) = v19;
          v73 = v8;
          if ( &v73 != (unsigned __int64 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v20 = v73;
            v21 = v74[0];
            a3[1] = v74[0];
            *a3 = v20;
            v8 = sub_14083D4F0(v21) + 8;
            v74[0] = 0;
            v73 = v8;
          }
          goto LABEL_72;
        }
        goto LABEL_118;
      }
    }
    else
    {
      if ( a2 == 1093755239 )
      {
        v25 = *(unsigned __int8 *)(a1 + 155);
        if ( (char)v25 > 0 )
        {
          v8 = sub_14083D4F0(a1) + 40;
          LODWORD(v74[0]) = v25;
          v73 = v8;
          if ( &v73 != (unsigned __int64 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v26 = v73;
            v27 = v74[0];
            a3[1] = v74[0];
            *a3 = v26;
            v8 = sub_14083D4F0(v27) + 8;
            v74[0] = 0;
            v73 = v8;
          }
          goto LABEL_72;
        }
        goto LABEL_118;
      }
      if ( a2 == 1093757234 )
      {
        v11 = *(unsigned __int16 *)(a1 + 144);
        if ( *(_WORD *)(a1 + 144) != 0 )
        {
          v8 = sub_14083D4F0(a1) + 40;
          LODWORD(v74[0]) = v11;
          v73 = v8;
          if ( &v73 != (unsigned __int64 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v12 = v73;
            v13 = v74[0];
            a3[1] = v74[0];
            *a3 = v12;
            v8 = sub_14083D4F0(v13) + 8;
            v74[0] = 0;
            v73 = v8;
          }
          goto LABEL_72;
        }
        goto LABEL_118;
      }
    }
    return sub_140FE3F20((_DWORD *)a1, a2, a3);
  }
  if ( a2 > 1095265891 )
  {
    if ( a2 > 1095266354 )
    {
      switch ( a2 )
      {
        case 1095266355:
          v47 = *(_DWORD *)(a1 + 136);
          if ( v47 != 0 )
          {
            v8 = sub_14083D4F0(a1) + 56;
            LODWORD(v74[0]) = v47;
            v73 = v8;
            if ( &v73 != (unsigned __int64 *)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v48 = v73;
              v49 = v74[0];
              a3[1] = v74[0];
              *a3 = v48;
              v8 = sub_14083D4F0(v49) + 8;
              v74[0] = 0;
              v73 = v8;
            }
            goto LABEL_72;
          }
          goto LABEL_118;
        case 1097363060:
          v50 = *(_BYTE *)(a1 + 158);
          v8 = sub_14083D4F0(a1) + 24;
          LOBYTE(v74[0]) = v50;
          v73 = v8;
          if ( &v73 != (unsigned __int64 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v51 = v73;
            v52 = v74[0];
            a3[1] = v74[0];
            *a3 = v51;
            v8 = sub_14083D4F0(v52) + 8;
            v74[0] = 0;
            v73 = v8;
          }
          goto LABEL_72;
        case 1095268709:
          v16 = *(__int16 *)(a1 + 140);
          v8 = sub_14083D4F0(a1) + 40;
          LODWORD(v74[0]) = v16;
          v73 = v8;
          if ( &v73 != (unsigned __int64 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v17 = v73;
            v18 = v74[0];
            a3[1] = v74[0];
            *a3 = v17;
            v8 = sub_14083D4F0(v18) + 8;
            v74[0] = 0;
            v73 = v8;
          }
          goto LABEL_72;
        default:
          break;
      }
    }
    else
    {
      switch ( a2 )
      {
        case 1095265892:
          v41 = *(_BYTE *)(a1 + 157);
          v8 = sub_14083D4F0(a1) + 24;
          LOBYTE(v74[0]) = v41;
          v73 = v8;
          if ( &v73 != (unsigned __int64 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v42 = v73;
            v43 = v74[0];
            a3[1] = v74[0];
            *a3 = v42;
            v8 = sub_14083D4F0(v43) + 8;
            v74[0] = 0;
            v73 = v8;
          }
          goto LABEL_72;
        case 1095266353:
          v44 = *(_DWORD *)(a1 + 128);
          if ( v44 != 0 )
          {
            v8 = sub_14083D4F0(a1) + 56;
            LODWORD(v74[0]) = v44;
            v73 = v8;
            if ( &v73 != (unsigned __int64 *)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v45 = v73;
              v46 = v74[0];
              a3[1] = v74[0];
              *a3 = v45;
              v8 = sub_14083D4F0(v46) + 8;
              v74[0] = 0;
              v73 = v8;
            }
            goto LABEL_72;
          }
          goto LABEL_118;
        case 1095266354:
          v7 = *(_DWORD *)(a1 + 132);
          if ( v7 != 0 )
          {
            v8 = sub_14083D4F0(a1) + 56;
            LODWORD(v74[0]) = v7;
            v73 = v8;
            if ( &v73 != (unsigned __int64 *)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v9 = v73;
              v10 = v74[0];
              a3[1] = v74[0];
              *a3 = v9;
              v8 = sub_14083D4F0(v10) + 8;
              v74[0] = 0;
              v73 = v8;
            }
            goto LABEL_72;
          }
LABEL_118:
          if ( a3 != &qword_141B5A4A0 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
              qword_141B5A4A0,
              &qword_141B5A4A0,
              a3);
          }
          return 1;
        default:
          break;
      }
    }
    return sub_140FE3F20((_DWORD *)a1, a2, a3);
  }
  switch ( a2 )
  {
    case 1095250531:
      v4 = *(_QWORD *)(a1 + 56);
      if ( v4 != 0 )
        goto LABEL_28;
      goto LABEL_10;
    case 1095250532:
    case 1095250533:
    case 1095250534:
    case 1095250535:
    case 1095250536:
    case 1095250538:
    case 1095250539:
    case 1095250540:
    case 1095250541:
    case 1095250543:
    case 1095250545:
    case 1095250546:
    case 1095250547:
      return sub_140FE3F20((_DWORD *)a1, a2, a3);
    case 1095250537:
      v31 = *(unsigned __int16 *)(a1 + 146);
      if ( *(_WORD *)(a1 + 146) == 0 )
        goto LABEL_118;
      v8 = sub_14083D4F0(a1) + 40;
      LODWORD(v74[0]) = v31;
      v73 = v8;
      if ( &v73 != (unsigned __int64 *)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v32 = v73;
        v33 = v74[0];
        a3[1] = v74[0];
        *a3 = v32;
        v8 = sub_14083D4F0(v33) + 8;
        v74[0] = 0;
        v73 = v8;
      }
      break;
    case 1095250542:
      v34 = (__int64 *)(a1 + 88);
      v35 = sub_14083D4F0(a1);
      v74[0] = 0;
      if ( v74 != v34 )
      {
        v36 = *v34;
        if ( *v34 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v36 - 4));
        v74[0] = v36;
      }
      v8 = v35 + 136;
      v73 = v8;
      if ( &v73 != (unsigned __int64 *)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v37 = v73;
        v38 = v74[0];
        a3[1] = v74[0];
        *a3 = v37;
        v8 = sub_14083D4F0(v38) + 8;
        v74[0] = 0;
        v73 = v8;
      }
      break;
    case 1095250544:
      v39 = *(_QWORD *)(a1 + 48);
      goto LABEL_110;
    case 1095250548:
      v40 = (unsigned __int64 *)(a1 + 112);
      goto LABEL_112;
    default:
      switch ( a2 )
      {
        case 1095250787:
          v4 = *(_QWORD *)(a1 + 64);
          if ( v4 == 0 )
            goto LABEL_10;
          goto LABEL_28;
        case 1095250793:
          v53 = *(unsigned __int16 *)(a1 + 150);
          if ( *(_WORD *)(a1 + 150) == 0 )
            goto LABEL_118;
          v8 = sub_14083D4F0(a1) + 40;
          LODWORD(v74[0]) = v53;
          v73 = v8;
          if ( &v73 != (unsigned __int64 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v54 = v73;
            v55 = v74[0];
            a3[1] = v74[0];
            *a3 = v54;
            v8 = sub_14083D4F0(v55) + 8;
            v74[0] = 0;
            v73 = v8;
          }
          break;
        case 1095250798:
          v56 = (__int64 *)(a1 + 96);
          v57 = sub_14083D4F0(a1);
          v74[0] = 0;
          if ( v74 != v56 )
          {
            v58 = *v56;
            if ( *v56 != 0 )
              _InterlockedIncrement((volatile signed __int32 *)(v58 - 4));
            v74[0] = v58;
          }
          v8 = v57 + 136;
          v73 = v8;
          if ( &v73 != (unsigned __int64 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v59 = v73;
            v60 = v74[0];
            a3[1] = v74[0];
            *a3 = v59;
            v8 = sub_14083D4F0(v60) + 8;
            v74[0] = 0;
            v73 = v8;
          }
          goto LABEL_72;
        case 1095250800:
          v39 = *(_QWORD *)(a1 + 72);
          goto LABEL_110;
        case 1095250804:
          v40 = (unsigned __int64 *)(a1 + 120);
          goto LABEL_112;
        default:
          return sub_140FE3F20((_DWORD *)a1, a2, a3);
      }
      break;
  }
LABEL_72:
  (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v8 + 16LL))(v8, &v73);
  return 1;
}
