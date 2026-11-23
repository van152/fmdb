char __fastcall sub_141581650(__int64 a1, int a2, __int64 *a3)
{
  int v4; // edi
  __int64 v5; // rax
  __int64 v6; // rax
  __int64 v7; // rcx
  int v8; // edi
  __int64 v9; // rax
  __int64 v10; // rcx
  __int64 *v11; // rdi
  __int64 v12; // rax
  __int64 v13; // rcx
  __int64 v14; // rax
  __int64 v15; // rcx
  char v16; // bl
  __int64 v17; // rax
  __int64 v18; // rcx
  __int64 *v19; // rdi
  __int64 v20; // rax
  __int64 v21; // rcx
  __int64 v22; // rax
  __int64 v23; // rcx
  char v24; // bl
  __int64 v25; // rax
  __int64 v26; // rcx
  int v27; // edi
  __int64 v28; // rax
  __int64 v29; // rcx
  int v30; // edi
  __int64 v31; // rax
  __int64 v32; // rcx
  int v33; // edi
  __int64 v34; // rax
  __int64 v35; // rcx
  int v36; // edi
  __int64 v37; // rax
  __int64 v38; // rcx
  char v39; // bl
  __int64 v40; // rax
  __int64 v41; // rcx
  char v42; // bl
  __int64 v43; // rax
  __int64 v44; // rcx
  int v45; // xmm6_4
  __int64 v46; // rax
  __int64 v47; // rcx
  char v48; // bl
  __int64 v49; // rax
  __int64 v50; // rcx
  char v51; // bl
  __int64 v52; // rax
  __int64 v53; // rcx
  char v54; // bl
  __int64 v55; // rax
  __int64 v56; // rcx
  int v57; // edi
  __int64 v58; // rax
  __int64 v59; // rcx
  int v60; // edi
  __int64 v61; // rax
  __int64 v62; // rcx
  int v63; // edi
  __int64 v64; // rax
  __int64 v65; // rcx
  int v66; // edi
  __int64 v67; // rax
  __int64 v68; // rcx
  int v69; // edi
  __int64 v70; // rax
  __int64 v71; // rcx
  int v72; // edi
  __int64 v73; // rax
  __int64 v74; // rcx
  char v75; // bl
  __int64 v76; // rax
  __int64 v77; // rcx
  __int64 v79; // [rsp+28h] [rbp-28h] BYREF
  _QWORD v80[2]; // [rsp+30h] [rbp-20h] BYREF

  v80[1] = -2;
  if ( a2 <= 1231386723 )
  {
    if ( a2 <= 1231188071 )
    {
      if ( a2 <= 1231186285 )
      {
        if ( a2 == 1145392197 )
        {
          v75 = *(_BYTE *)(a1 + 76);
          v5 = sub_14083D4F0(a1) + 24;
          LOBYTE(v80[0]) = v75 == -2;
          v79 = v5;
          if ( &v79 != a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v76 = v79;
            v77 = v80[0];
            a3[1] = v80[0];
            *a3 = v76;
            v5 = sub_14083D4F0(v77) + 8;
            v80[0] = 0;
            v79 = v5;
          }
          goto LABEL_103;
        }
        if ( a2 == 1231120242 )
        {
          v30 = *(char *)(a1 + 81);
          v5 = sub_14083D4F0(a1) + 40;
          LODWORD(v80[0]) = v30;
          v79 = v5;
          if ( &v79 != a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v31 = v79;
            v32 = v80[0];
            a3[1] = v80[0];
            *a3 = v31;
            v5 = sub_14083D4F0(v32) + 8;
            v80[0] = 0;
            v79 = v5;
          }
          goto LABEL_103;
        }
      }
      else
      {
        switch ( a2 )
        {
          case 1231186286:
            v51 = *(_BYTE *)(a1 + 87);
            v5 = sub_14083D4F0(a1) + 24;
            LOBYTE(v80[0]) = (v51 & 4) != 0;
            v79 = v5;
            if ( &v79 != a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v52 = v79;
              v53 = v80[0];
              a3[1] = v80[0];
              *a3 = v52;
              v5 = sub_14083D4F0(v53) + 8;
              v80[0] = 0;
              v79 = v5;
            }
            goto LABEL_103;
          case 1231186291:
            v54 = *(_BYTE *)(a1 + 87);
            v5 = sub_14083D4F0(a1) + 24;
            LOBYTE(v80[0]) = (v54 & 8) != 0;
            v79 = v5;
            if ( &v79 != a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v55 = v79;
              v56 = v80[0];
              a3[1] = v80[0];
              *a3 = v55;
              v5 = sub_14083D4F0(v56) + 8;
              v80[0] = 0;
              v79 = v5;
            }
            goto LABEL_103;
          case 1231188071:
            v16 = *(_BYTE *)(a1 + 87);
            v5 = sub_14083D4F0(a1) + 24;
            LOBYTE(v80[0]) = (v16 & 0x10) != 0;
            v79 = v5;
            if ( &v79 != a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v17 = v79;
              v18 = v80[0];
              a3[1] = v80[0];
              *a3 = v17;
              v5 = sub_14083D4F0(v18) + 8;
              v80[0] = 0;
              v79 = v5;
            }
            goto LABEL_103;
          default:
            break;
        }
      }
    }
    else if ( a2 > 1231250543 )
    {
      switch ( a2 )
      {
        case 1231250544:
          v63 = *(unsigned __int8 *)(a1 + 86);
          if ( (v63 & 0x80u) == 0 )
          {
            v5 = sub_14083D4F0(a1) + 40;
            LODWORD(v80[0]) = v63;
            v79 = v5;
            if ( &v79 != a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v64 = v79;
              v65 = v80[0];
              a3[1] = v80[0];
              *a3 = v64;
              v5 = sub_14083D4F0(v65) + 8;
              v80[0] = 0;
              v79 = v5;
            }
            goto LABEL_103;
          }
          goto LABEL_111;
        case 1231252851:
          v66 = *(char *)(a1 + 82);
          v5 = sub_14083D4F0(a1) + 40;
          LODWORD(v80[0]) = v66;
          v79 = v5;
          if ( &v79 != a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v67 = v79;
            v68 = v80[0];
            a3[1] = v80[0];
            *a3 = v67;
            v5 = sub_14083D4F0(v68) + 8;
            v80[0] = 0;
            v79 = v5;
          }
          goto LABEL_103;
        case 1231253358:
          v24 = *(_BYTE *)(a1 + 83);
          v5 = sub_14083D4F0(a1) + 24;
          LOBYTE(v80[0]) = v24;
          v79 = v5;
          if ( &v79 != a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v25 = v79;
            v26 = v80[0];
            a3[1] = v80[0];
            *a3 = v25;
            v5 = sub_14083D4F0(v26) + 8;
            v80[0] = 0;
            v79 = v5;
          }
          goto LABEL_103;
        default:
          break;
      }
    }
    else
    {
      switch ( a2 )
      {
        case 1231188072:
          v39 = *(_BYTE *)(a1 + 87) & 1;
          v5 = sub_14083D4F0(a1) + 24;
          LOBYTE(v80[0]) = v39;
          v79 = v5;
          if ( &v79 != a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v40 = v79;
            v41 = v80[0];
            a3[1] = v80[0];
            *a3 = v40;
            v5 = sub_14083D4F0(v41) + 8;
            v80[0] = 0;
            v79 = v5;
          }
          goto LABEL_103;
        case 1231188848:
          v42 = *(_BYTE *)(a1 + 87);
          v5 = sub_14083D4F0(a1) + 24;
          LOBYTE(v80[0]) = (v42 & 2) != 0;
          v79 = v5;
          if ( &v79 != a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v43 = v79;
            v44 = v80[0];
            a3[1] = v80[0];
            *a3 = v43;
            v5 = sub_14083D4F0(v44) + 8;
            v80[0] = 0;
            v79 = v5;
          }
          goto LABEL_103;
        case 1231249781:
          v8 = *(__int16 *)(a1 + 78);
          v5 = sub_14083D4F0(a1) + 40;
          LODWORD(v80[0]) = v8;
          v79 = v5;
          if ( &v79 != a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v9 = v79;
            v10 = v80[0];
            a3[1] = v80[0];
            *a3 = v9;
            v5 = sub_14083D4F0(v10) + 8;
            v80[0] = 0;
            v79 = v5;
          }
          goto LABEL_103;
        default:
          break;
      }
    }
    return sub_140FE3F20((_DWORD *)a1, a2, a3);
  }
  if ( a2 > 1232036721 )
  {
    if ( a2 > 1768123488 )
    {
      switch ( a2 )
      {
        case 1768123489:
          v69 = *(char *)(a1 + 76);
          v5 = sub_14083D4F0(a1) + 40;
          LODWORD(v80[0]) = v69;
          v79 = v5;
          if ( &v79 != a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v70 = v79;
            v71 = v80[0];
            a3[1] = v80[0];
            *a3 = v70;
            v5 = sub_14083D4F0(v71) + 8;
            v80[0] = 0;
            v79 = v5;
          }
          goto LABEL_103;
        case 1768838002:
          v72 = *(char *)(a1 + 84);
          v5 = sub_14083D4F0(a1) + 40;
          LODWORD(v80[0]) = v72;
          v79 = v5;
          if ( &v79 != a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v73 = v79;
            v74 = v80[0];
            a3[1] = v80[0];
            *a3 = v73;
            v5 = sub_14083D4F0(v74) + 8;
            v80[0] = 0;
            v79 = v5;
          }
          goto LABEL_103;
        case 1769169772:
          v27 = *(char *)(a1 + 77);
          v5 = sub_14083D4F0(a1) + 40;
          LODWORD(v80[0]) = v27;
          v79 = v5;
          if ( &v79 != a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v28 = v79;
            v29 = v80[0];
            a3[1] = v80[0];
            *a3 = v28;
            v5 = sub_14083D4F0(v29) + 8;
            v80[0] = 0;
            v79 = v5;
          }
          goto LABEL_103;
        default:
          break;
      }
    }
    else
    {
      switch ( a2 )
      {
        case 1232036722:
          v45 = *(_DWORD *)(a1 + 48);
          v5 = sub_14083D4F0(a1) + 104;
          LODWORD(v80[0]) = v45;
          v79 = v5;
          if ( &v79 != a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v46 = v79;
            v47 = v80[0];
            a3[1] = v80[0];
            *a3 = v46;
            v5 = sub_14083D4F0(v47) + 8;
            v80[0] = 0;
            v79 = v5;
          }
          goto LABEL_103;
        case 1232233827:
          v48 = *(_BYTE *)(a1 + 89);
          v5 = sub_14083D4F0(a1) + 24;
          LOBYTE(v80[0]) = v48;
          v79 = v5;
          if ( &v79 != a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v49 = v79;
            v50 = v80[0];
            a3[1] = v80[0];
            *a3 = v49;
            v5 = sub_14083D4F0(v50) + 8;
            v80[0] = 0;
            v79 = v5;
          }
          goto LABEL_103;
        case 1232301677:
          v11 = (__int64 *)(a1 + 32);
          v12 = sub_14083D4F0(a1);
          v80[0] = 0;
          if ( v80 != v11 )
          {
            v13 = *v11;
            if ( *v11 != 0 )
              _InterlockedIncrement((volatile signed __int32 *)(v13 - 4));
            v80[0] = v13;
          }
          v5 = v12 + 136;
          v79 = v5;
          if ( &v79 != a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v14 = v79;
            v15 = v80[0];
            a3[1] = v80[0];
            *a3 = v14;
            v5 = sub_14083D4F0(v15) + 8;
            v80[0] = 0;
            v79 = v5;
          }
          goto LABEL_103;
        default:
          break;
      }
    }
    return sub_140FE3F20((_DWORD *)a1, a2, a3);
  }
  if ( a2 > 1231907183 )
  {
    switch ( a2 )
    {
      case 1231907184:
        v57 = *(char *)(a1 + 80);
        v5 = sub_14083D4F0(a1) + 40;
        LODWORD(v80[0]) = v57;
        v79 = v5;
        if ( &v79 != a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v58 = v79;
          v59 = v80[0];
          a3[1] = v80[0];
          *a3 = v58;
          v5 = sub_14083D4F0(v59) + 8;
          v80[0] = 0;
          v79 = v5;
        }
        goto LABEL_103;
      case 1231908452:
        v60 = *(__int16 *)(a1 + 52);
        v5 = sub_14083D4F0(a1) + 40;
        LODWORD(v80[0]) = v60;
        v79 = v5;
        if ( &v79 != a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v61 = v79;
          v62 = v80[0];
          a3[1] = v80[0];
          *a3 = v61;
          v5 = sub_14083D4F0(v62) + 8;
          v80[0] = 0;
          v79 = v5;
        }
        goto LABEL_103;
      case 1231970669:
        v19 = (__int64 *)(a1 + 24);
        v20 = sub_14083D4F0(a1);
        v80[0] = 0;
        if ( v80 != v19 )
        {
          v21 = *v19;
          if ( *v19 != 0 )
            _InterlockedIncrement((volatile signed __int32 *)(v21 - 4));
          v80[0] = v21;
        }
        v5 = v20 + 136;
        v79 = v5;
        if ( &v79 != a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v22 = v79;
          v23 = v80[0];
          a3[1] = v80[0];
          *a3 = v22;
          v5 = sub_14083D4F0(v23) + 8;
          v80[0] = 0;
          v79 = v5;
        }
        goto LABEL_103;
      default:
        break;
    }
    return sub_140FE3F20((_DWORD *)a1, a2, a3);
  }
  if ( a2 == 1231386724 )
  {
    v33 = *(__int16 *)(a1 + 54);
    v5 = sub_14083D4F0(a1) + 40;
    LODWORD(v80[0]) = v33;
    v79 = v5;
    if ( &v79 != a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v34 = v79;
      v35 = v80[0];
      a3[1] = v80[0];
      *a3 = v34;
      v5 = sub_14083D4F0(v35) + 8;
      v80[0] = 0;
      v79 = v5;
    }
    goto LABEL_103;
  }
  if ( a2 == 1231515762 )
  {
    v36 = *(unsigned __int8 *)(a1 + 85);
    if ( (v36 & 0x80u) == 0 )
    {
      v5 = sub_14083D4F0(a1) + 40;
      LODWORD(v80[0]) = v36;
      v79 = v5;
      if ( &v79 != a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v37 = v79;
        v38 = v80[0];
        a3[1] = v80[0];
        *a3 = v37;
        v5 = sub_14083D4F0(v38) + 8;
        v80[0] = 0;
        v79 = v5;
      }
      goto LABEL_103;
    }
LABEL_111:
    if ( a3 != &qword_141B5A4A0 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
        qword_141B5A4A0,
        &qword_141B5A4A0,
        a3);
    }
    return 1;
  }
  if ( a2 != 1231642994 )
    return sub_140FE3F20((_DWORD *)a1, a2, a3);
  v4 = *(char *)(a1 + 88);
  v5 = sub_14083D4F0(a1) + 40;
  LODWORD(v80[0]) = v4;
  v79 = v5;
  if ( &v79 != a3 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
    v6 = v79;
    v7 = v80[0];
    a3[1] = v80[0];
    *a3 = v6;
    v5 = sub_14083D4F0(v7) + 8;
    v80[0] = 0;
    v79 = v5;
  }
LABEL_103:
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v5 + 16LL))(v5, &v79);
  return 1;
}
