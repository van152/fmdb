__int64 __fastcall sub_141455810(__int64 a1, int a2, unsigned __int64 *a3)
{
  __int64 v5; // rbx
  int v6; // ebx
  __int64 v7; // rax
  unsigned __int64 v8; // rax
  unsigned __int64 v9; // rcx
  int v10; // ebx
  __int64 v11; // rax
  unsigned __int64 v12; // rax
  unsigned __int64 v13; // rcx
  int v14; // ebx
  __int64 v15; // rax
  unsigned __int64 v16; // rax
  unsigned __int64 v17; // rcx
  int v18; // eax
  int v19; // edi
  __int64 v20; // rax
  int v21; // ecx
  char v22; // bl
  __int64 v23; // rax
  unsigned __int64 v24; // rax
  unsigned __int64 v25; // rcx
  int v26; // edi
  unsigned __int64 v27; // rax
  unsigned __int64 v28; // rcx
  int v29; // ebx
  __int64 v30; // rax
  unsigned __int64 v31; // rax
  unsigned __int64 v32; // rcx
  int v33; // edi
  unsigned __int64 v34; // rax
  unsigned __int64 v35; // rcx
  int v36; // edi
  __int64 v37; // rax
  int v38; // ecx
  int v39; // ebx
  __int64 v40; // rax
  unsigned __int64 v41; // rax
  unsigned __int64 v42; // rcx
  __int64 v43; // rdx
  unsigned __int64 v45; // [rsp+20h] [rbp-10h] BYREF
  unsigned __int64 v46; // [rsp+28h] [rbp-8h]
  __int64 v47; // [rsp+30h] [rbp+0h]

  v47 = -2;
  LODWORD(v5) = 0;
  if ( a2 <= 1835820397 )
  {
    if ( a2 > 1769172838 )
    {
      switch ( a2 )
      {
        case 1769172839:
          v22 = *(_BYTE *)(a1 + 58);
          v23 = sub_14083D4F0(a1) + 24;
          LOBYTE(v46) = v22;
          v45 = v23;
          if ( &v45 != a3 )
          {
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v24 = v45;
            v25 = v46;
            a3[1] = v46;
            *a3 = v24;
            v23 = sub_14083D4F0(v25) + 8;
            v46 = 0;
            v45 = v23;
          }
          break;
        case 1818588780:
          v26 = *(char *)(a1 + 55);
          v23 = sub_14083D4F0(a1) + 40;
          LODWORD(v46) = v26;
          v45 = v23;
          if ( &v45 != a3 )
          {
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v27 = v45;
            v28 = v46;
            a3[1] = v46;
            *a3 = v27;
            v23 = sub_14083D4F0(v28) + 8;
            v46 = 0;
            v45 = v23;
          }
          break;
        case 1835100005:
          v6 = *(char *)(a1 + 56);
          v7 = sub_14083D4F0(a1) + 40;
          LODWORD(v46) = v6;
          v45 = v7;
          if ( &v45 != a3 )
          {
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v8 = v45;
            v9 = v46;
            a3[1] = v46;
            *a3 = v8;
            v7 = sub_14083D4F0(v9) + 8;
            v46 = 0;
            v45 = v7;
          }
          v5 = *(_QWORD *)v7;
          (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v7 + 16LL))(v7, &v45);
          LOBYTE(v5) = 1;
          if ( a3 == (unsigned __int64 *)&qword_141B5A4A0 || *(_BYTE *)(a1 + 56) != 0 )
            return (unsigned int)v5;
LABEL_57:
          (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          (*(void (__fastcall **)(__int64, __int64 *, unsigned __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
            qword_141B5A4A0,
            &qword_141B5A4A0,
            a3);
          return (unsigned int)v5;
        default:
          return (unsigned int)v5;
      }
      goto LABEL_47;
    }
    if ( a2 != 1668246896 )
    {
      if ( a2 == 1701738866 )
      {
        v14 = *(unsigned __int16 *)(a1 + 52);
        v15 = sub_14083D4F0(a1) + 40;
        LODWORD(v46) = v14;
        v45 = v15;
        if ( &v45 != a3 )
        {
          (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v16 = v45;
          v17 = v46;
          a3[1] = v46;
          *a3 = v16;
          v15 = sub_14083D4F0(v17) + 8;
          v46 = 0;
          v45 = v15;
        }
        v5 = *(_QWORD *)v15;
        (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v15 + 16LL))(v15, &v45);
        LOBYTE(v5) = 1;
        if ( a3 != (unsigned __int64 *)&qword_141B5A4A0 )
        {
          v18 = *(unsigned __int16 *)(a1 + 52);
          goto LABEL_43;
        }
      }
      return (unsigned int)v5;
    }
    v36 = -1;
    if ( *(_DWORD *)(a1 + 40) == -1 )
    {
      v38 = -1;
    }
    else
    {
      v37 = sub_140F45DB0(qword_141B5FDC0);
      v38 = -1;
      if ( v37 != 0 )
      {
        v36 = *(_DWORD *)(v37 + 12);
        v38 = *(_DWORD *)(v37 + 16);
        if ( v38 == 0 )
          v38 = *(_DWORD *)(v37 + 12);
      }
    }
    v45 = __PAIR64__(v38, v36);
    v43 = 1668246896;
LABEL_62:
    sub_140FE72B0(&v45, v43, a3);
    goto LABEL_63;
  }
  if ( a2 <= 1937013105 )
  {
    if ( a2 == 1835820398 )
    {
      v39 = *(char *)(a1 + 57);
      v40 = sub_14083D4F0(a1) + 40;
      LODWORD(v46) = v39;
      v45 = v40;
      if ( &v45 != a3 )
      {
        (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v41 = v45;
        v42 = v46;
        a3[1] = v46;
        *a3 = v41;
        v40 = sub_14083D4F0(v42) + 8;
        v46 = 0;
        v45 = v40;
      }
      v5 = *(_QWORD *)v40;
      (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v40 + 16LL))(v40, &v45);
      LOBYTE(v5) = 1;
      if ( a3 != (unsigned __int64 *)&qword_141B5A4A0 && *(_BYTE *)(a1 + 57) == 0 )
        goto LABEL_57;
      return (unsigned int)v5;
    }
    if ( a2 != 1851880553 )
      return (unsigned int)v5;
    v19 = -1;
    if ( *(_DWORD *)(a1 + 44) == -1 )
    {
      v21 = -1;
    }
    else
    {
      v20 = sub_1400568B0(qword_141B5FDD0);
      v21 = -1;
      if ( v20 != 0 )
      {
        v19 = *(_DWORD *)(v20 + 12);
        v21 = *(_DWORD *)(v20 + 16);
        if ( v21 == 0 )
          v21 = *(_DWORD *)(v20 + 12);
      }
    }
    v45 = __PAIR64__(v21, v19);
    v43 = 1315856756;
    goto LABEL_62;
  }
  switch ( a2 )
  {
    case 1937013106:
      v29 = *(unsigned __int16 *)(a1 + 50);
      v30 = sub_14083D4F0(a1) + 40;
      LODWORD(v46) = v29;
      v45 = v30;
      if ( &v45 != a3 )
      {
        (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v31 = v45;
        v32 = v46;
        a3[1] = v46;
        *a3 = v31;
        v30 = sub_14083D4F0(v32) + 8;
        v46 = 0;
        v45 = v30;
      }
      v5 = *(_QWORD *)v30;
      (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v30 + 16LL))(v30, &v45);
      LOBYTE(v5) = 1;
      if ( a3 != (unsigned __int64 *)&qword_141B5A4A0 )
      {
        v18 = *(unsigned __int16 *)(a1 + 50);
LABEL_43:
        if ( v18 != 1900 )
          return (unsigned int)v5;
        goto LABEL_57;
      }
      break;
    case 2003985260:
      v33 = *(__int16 *)(a1 + 48);
      v23 = sub_14083D4F0(a1) + 40;
      LODWORD(v46) = v33;
      v45 = v23;
      if ( &v45 != a3 )
      {
        (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v34 = v45;
        v35 = v46;
        a3[1] = v46;
        *a3 = v34;
        v23 = sub_14083D4F0(v35) + 8;
        v46 = 0;
        v45 = v23;
      }
LABEL_47:
      v5 = *(_QWORD *)v23;
      (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v23 + 16LL))(v23, &v45);
LABEL_63:
      LOBYTE(v5) = 1;
      return (unsigned int)v5;
    case 1954115685:
      v10 = *(unsigned __int8 *)(a1 + 54);
      v11 = sub_14083D4F0(a1) + 56;
      LODWORD(v46) = v10;
      v45 = v11;
      if ( &v45 != a3 )
      {
        (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v12 = v45;
        v13 = v46;
        a3[1] = v46;
        *a3 = v12;
        v11 = sub_14083D4F0(v13) + 8;
        v46 = 0;
        v45 = v11;
      }
      v5 = *(_QWORD *)v11;
      (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v11 + 16LL))(v11, &v45);
      LOBYTE(v5) = 1;
      if ( a3 != (unsigned __int64 *)&qword_141B5A4A0 && *(_BYTE *)(a1 + 54) == 0 )
        goto LABEL_57;
      break;
    default:
      break;
  }
  return (unsigned int)v5;
}
