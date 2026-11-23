__int64 __fastcall sub_141570250(__int64 a1, int a2, unsigned __int64 *a3)
{
  __int64 v4; // rdi
  __int64 v5; // rcx
  int v6; // eax
  int v7; // ecx
  int v8; // edi
  char v9; // al
  __int64 v10; // rcx
  int v11; // eax
  int v12; // ecx
  __int64 v13; // rdx
  int v14; // edi
  __int64 v15; // rax
  unsigned __int64 v16; // rax
  unsigned __int64 v17; // rcx
  __int64 v18; // rcx
  int v19; // eax
  int v20; // ecx
  unsigned __int64 v21; // rax
  unsigned __int64 v22; // rcx
  int v23; // edi
  unsigned __int64 v24; // rax
  unsigned __int64 v25; // rcx
  unsigned __int64 v27; // rax
  unsigned __int64 v28; // rcx
  unsigned __int64 v29; // [rsp+28h] [rbp-18h] BYREF
  unsigned __int64 v30; // [rsp+30h] [rbp-10h]
  __int64 v31; // [rsp+38h] [rbp-8h]

  v31 = -2;
  LODWORD(v4) = 0;
  if ( a2 > 1886352232 )
  {
    if ( a2 > 1937013105 )
    {
      if ( a2 != 1937013106 )
      {
        if ( a2 == 1952673648 )
        {
          v18 = *(_QWORD *)(a1 + 64);
          if ( v18 != 0 )
          {
            v19 = *(_DWORD *)(v18 + 12);
            v20 = *(_DWORD *)(v18 + 16);
            if ( v20 == 0 )
              v20 = v19;
          }
          else
          {
            v19 = -1;
            v20 = -1;
          }
          v29 = __PAIR64__(v20, v19);
          v13 = 1416914273;
          goto LABEL_45;
        }
        if ( a2 == 1952671843 )
        {
          v5 = *(_QWORD *)(a1 + 24);
          if ( v5 != 0 )
            goto LABEL_7;
          goto LABEL_34;
        }
        return (unsigned int)v4;
      }
      v14 = *(unsigned __int16 *)(a1 + 72);
      v15 = sub_14083D4F0(a1) + 40;
      LODWORD(v30) = v14;
      v29 = v15;
      if ( &v29 != a3 )
      {
        (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v16 = v29;
        v17 = v30;
        a3[1] = v30;
        *a3 = v16;
        v15 = sub_14083D4F0(v17) + 8;
        v30 = 0;
        v29 = v15;
      }
LABEL_61:
      v4 = *(_QWORD *)v15;
      (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v15 + 16LL))(v15, &v29);
      goto LABEL_46;
    }
    if ( a2 == 1886352233 )
    {
      LODWORD(v4) = *(char *)(a1 + 78);
      if ( (_DWORD)v4 == -1 )
      {
        LOBYTE(v4) = 1;
        if ( a3 != (unsigned __int64 *)&qword_141B5A4A0 )
        {
          (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          (*(void (__fastcall **)(__int64, __int64 *, unsigned __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
            qword_141B5A4A0,
            &qword_141B5A4A0,
            a3);
        }
        return (unsigned int)v4;
      }
      v15 = sub_14083D4F0(a1) + 40;
      LODWORD(v30) = v4;
      v29 = v15;
      if ( &v29 != a3 )
      {
        (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v21 = v29;
        v22 = v30;
        a3[1] = v30;
        *a3 = v21;
        v15 = sub_14083D4F0(v22) + 8;
        v30 = 0;
        v29 = v15;
      }
      goto LABEL_61;
    }
    if ( a2 != 1936946286 )
      return (unsigned int)v4;
    v10 = *(_QWORD *)(a1 + 56);
    if ( v10 != 0 )
      goto LABEL_18;
    goto LABEL_24;
  }
  if ( a2 > 1701083505 )
  {
    if ( a2 == 1701083506 )
    {
      v23 = *(unsigned __int16 *)(a1 + 74);
      v15 = sub_14083D4F0(a1) + 40;
      LODWORD(v30) = v23;
      v29 = v15;
      if ( &v29 != a3 )
      {
        (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v24 = v29;
        v25 = v30;
        a3[1] = v30;
        *a3 = v24;
        v15 = sub_14083D4F0(v25) + 8;
        v30 = 0;
        v29 = v15;
      }
      goto LABEL_61;
    }
    if ( a2 != 1836282990 )
      return (unsigned int)v4;
    v10 = *(_QWORD *)(a1 + 48);
    if ( v10 != 0 )
    {
LABEL_18:
      v11 = *(_DWORD *)(v10 + 12);
      v12 = *(_DWORD *)(v10 + 16);
      if ( v12 == 0 )
        v12 = v11;
      goto LABEL_25;
    }
LABEL_24:
    v11 = -1;
    v12 = -1;
LABEL_25:
    v29 = __PAIR64__(v12, v11);
    v13 = 1937008494;
LABEL_45:
    sub_140FE72B0(&v29, v13, a3);
LABEL_46:
    LOBYTE(v4) = 1;
    return (unsigned int)v4;
  }
  if ( a2 == 1668380006 )
  {
    v5 = *(_QWORD *)(a1 + 40);
    if ( v5 != 0 )
    {
LABEL_7:
      v6 = *(_DWORD *)(v5 + 12);
      v7 = *(_DWORD *)(v5 + 16);
      if ( v7 == 0 )
        v7 = v6;
      goto LABEL_35;
    }
LABEL_34:
    v6 = -1;
    v7 = -1;
LABEL_35:
    v29 = __PAIR64__(v7, v6);
    v13 = 1668246896;
    goto LABEL_45;
  }
  if ( a2 == 1684173428 )
  {
    v8 = 0;
    v9 = *(_BYTE *)(a1 + 76);
    switch ( *(_BYTE *)(a1 + 77) )
    {
      case 1:
        a1 = v9 == 0;
        v8 = 9 * a1 + 1;
        break;
      case 2:
        a1 = v9 == 0;
        v8 = 9 * a1 + 2;
        break;
      case 3:
        a1 = v9 == 0;
        v8 = 9 * a1 + 3;
        break;
      case 4:
        a1 = v9 == 0;
        v8 = 9 * a1 + 4;
        break;
      case 5:
        a1 = v9 == 0;
        v8 = 9 * a1 + 5;
        break;
      case 6:
        a1 = v9 == 0;
        v8 = 9 * a1 + 6;
        break;
      case 7:
        a1 = v9 == 0;
        v8 = 9 * a1 + 7;
        break;
      case 8:
        a1 = v9 == 0;
        v8 = 9 * a1 + 8;
        break;
      case 0xB:
        a1 = v9 == 0;
        v8 = 9 * a1 + 9;
        break;
      case 0xC:
        v8 = 19;
        break;
      default:
        break;
    }
    v15 = sub_14083D4F0(a1) + 40;
    LODWORD(v30) = v8;
    v29 = v15;
    if ( &v29 != a3 )
    {
      (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v27 = v29;
      v28 = v30;
      a3[1] = v30;
      *a3 = v27;
      v15 = sub_14083D4F0(v28) + 8;
      v30 = 0;
      v29 = v15;
    }
    goto LABEL_61;
  }
  return (unsigned int)v4;
}
