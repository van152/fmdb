__int64 __fastcall sub_14119F210(__int64 a1, int a2, unsigned __int64 *a3)
{
  __int64 v4; // rdi
  __int64 v5; // rax
  unsigned __int64 v6; // rax
  unsigned __int64 v7; // rcx
  unsigned __int64 v8; // rax
  unsigned __int64 v9; // rcx
  unsigned __int64 v10; // rax
  unsigned __int64 v11; // rcx
  int v12; // edi
  unsigned __int64 v13; // rax
  unsigned __int64 v14; // rcx
  __int64 v15; // rcx
  int v16; // eax
  int v17; // ecx
  unsigned __int64 v18; // rax
  unsigned __int64 v19; // rcx
  unsigned __int64 v20; // rax
  unsigned __int64 v21; // rcx
  unsigned __int64 v22; // rax
  unsigned __int64 v23; // rcx
  unsigned __int64 v24; // rax
  unsigned __int64 v25; // rcx
  unsigned __int64 v26; // rax
  unsigned __int64 v27; // rcx
  unsigned __int64 v28; // rax
  unsigned __int64 v29; // rcx
  unsigned __int64 v30; // rax
  unsigned __int64 v31; // rcx
  unsigned __int64 v33; // [rsp+28h] [rbp-18h] BYREF
  unsigned __int64 v34; // [rsp+30h] [rbp-10h]
  __int64 v35; // [rsp+38h] [rbp-8h]

  v35 = -2;
  LODWORD(v4) = 0;
  if ( a2 <= 1869767780 )
  {
    if ( a2 > 1734766449 )
    {
      switch ( a2 )
      {
        case 1734766450:
          LODWORD(v4) = *(__int16 *)(a1 + 48);
          if ( (_DWORD)v4 != -1 )
          {
            v5 = sub_14083D4F0(a1) + 40;
            LODWORD(v34) = v4;
            v33 = v5;
            if ( &v33 != a3 )
            {
              (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v24 = v33;
              v25 = v34;
              a3[1] = v34;
              *a3 = v24;
              v5 = sub_14083D4F0(v25) + 8;
              v34 = 0;
              v33 = v5;
            }
            goto LABEL_62;
          }
          break;
        case 1819243380:
          LODWORD(v4) = *(char *)(a1 + 61);
          if ( (_DWORD)v4 != -1 )
          {
            v5 = sub_14083D4F0(a1) + 40;
            LODWORD(v34) = v4;
            v33 = v5;
            if ( &v33 != a3 )
            {
              (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v26 = v33;
              v27 = v34;
              a3[1] = v34;
              *a3 = v26;
              v5 = sub_14083D4F0(v27) + 8;
              v34 = 0;
              v33 = v5;
            }
            goto LABEL_62;
          }
          break;
        case 1836610669:
          LODWORD(v4) = *(char *)(a1 + 62);
          if ( (_DWORD)v4 != -1 )
          {
            v5 = sub_14083D4F0(a1) + 40;
            LODWORD(v34) = v4;
            v33 = v5;
            if ( &v33 != a3 )
            {
              (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v10 = v33;
              v11 = v34;
              a3[1] = v34;
              *a3 = v10;
              v5 = sub_14083D4F0(v11) + 8;
              v34 = 0;
              v33 = v5;
            }
            goto LABEL_62;
          }
          break;
        default:
          return (unsigned int)v4;
      }
    }
    else
    {
      switch ( a2 )
      {
        case 1684633193:
          v15 = *(_QWORD *)(a1 + 24);
          if ( v15 != 0 )
          {
            v16 = *(_DWORD *)(v15 + 12);
            v17 = *(_DWORD *)(v15 + 16);
            if ( v17 == 0 )
              v17 = v16;
          }
          else
          {
            v16 = -1;
            v17 = -1;
          }
          v33 = __PAIR64__(v17, v16);
          sub_140FE72B0(&v33, 1668246896, a3);
          goto LABEL_67;
        case 1685217655:
          LODWORD(v4) = *(char *)(a1 + 60);
          if ( (_DWORD)v4 != -1 )
          {
            v5 = sub_14083D4F0(a1) + 40;
            LODWORD(v34) = v4;
            v33 = v5;
            if ( &v33 != a3 )
            {
              (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v18 = v33;
              v19 = v34;
              a3[1] = v34;
              *a3 = v18;
              v5 = sub_14083D4F0(v19) + 8;
              v34 = 0;
              v33 = v5;
            }
            goto LABEL_62;
          }
          break;
        case 1734436705:
          LODWORD(v4) = *(__int16 *)(a1 + 50);
          if ( (_DWORD)v4 != -1 )
          {
            v5 = sub_14083D4F0(a1) + 40;
            LODWORD(v34) = v4;
            v33 = v5;
            if ( &v33 != a3 )
            {
              (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v6 = v33;
              v7 = v34;
              a3[1] = v34;
              *a3 = v6;
              v5 = sub_14083D4F0(v7) + 8;
              v34 = 0;
              v33 = v5;
            }
LABEL_62:
            v4 = *(_QWORD *)v5;
            (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v5 + 16LL))(v5, &v33);
LABEL_67:
            LOBYTE(v4) = 1;
            return (unsigned int)v4;
          }
          break;
        default:
          return (unsigned int)v4;
      }
    }
    goto LABEL_63;
  }
  if ( a2 <= 1886352232 )
  {
    switch ( a2 )
    {
      case 1869767781:
        LODWORD(v4) = *(char *)(a1 + 56);
        if ( *(_BYTE *)(a1 + 56) != 0 )
        {
          v5 = sub_14083D4F0(a1) + 40;
          LODWORD(v34) = v4;
          v33 = v5;
          if ( &v33 != a3 )
          {
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v20 = v33;
            v21 = v34;
            a3[1] = v34;
            *a3 = v20;
            v5 = sub_14083D4F0(v21) + 8;
            v34 = 0;
            v33 = v5;
          }
          goto LABEL_62;
        }
        break;
      case 1886151033:
        LODWORD(v4) = *(char *)(a1 + 58);
        if ( (_DWORD)v4 != -1 )
        {
          v5 = sub_14083D4F0(a1) + 40;
          LODWORD(v34) = v4;
          v33 = v5;
          if ( &v33 != a3 )
          {
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v22 = v33;
            v23 = v34;
            a3[1] = v34;
            *a3 = v22;
            v5 = sub_14083D4F0(v23) + 8;
            v34 = 0;
            v33 = v5;
          }
          goto LABEL_62;
        }
        break;
      case 1886349678:
        LODWORD(v4) = *(__int16 *)(a1 + 52);
        if ( (_DWORD)v4 != -1 )
        {
          v5 = sub_14083D4F0(a1) + 40;
          LODWORD(v34) = v4;
          v33 = v5;
          if ( &v33 != a3 )
          {
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v8 = v33;
            v9 = v34;
            a3[1] = v34;
            *a3 = v8;
            v5 = sub_14083D4F0(v9) + 8;
            v34 = 0;
            v33 = v5;
          }
          goto LABEL_62;
        }
        break;
      default:
        return (unsigned int)v4;
    }
    goto LABEL_63;
  }
  switch ( a2 )
  {
    case 1886352233:
      LODWORD(v4) = *(char *)(a1 + 57);
      if ( (_DWORD)v4 != -1 )
      {
        v5 = sub_14083D4F0(a1) + 40;
        LODWORD(v34) = v4;
        v33 = v5;
        if ( &v33 != a3 )
        {
          (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v28 = v33;
          v29 = v34;
          a3[1] = v34;
          *a3 = v28;
          v5 = sub_14083D4F0(v29) + 8;
          v34 = 0;
          v33 = v5;
        }
        goto LABEL_62;
      }
LABEL_63:
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
    case 2003398259:
      LODWORD(v4) = *(char *)(a1 + 59);
      if ( (_DWORD)v4 != -1 )
      {
        v5 = sub_14083D4F0(a1) + 40;
        LODWORD(v34) = v4;
        v33 = v5;
        if ( &v33 != a3 )
        {
          (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v30 = v33;
          v31 = v34;
          a3[1] = v34;
          *a3 = v30;
          v5 = sub_14083D4F0(v31) + 8;
          v34 = 0;
          v33 = v5;
        }
        goto LABEL_62;
      }
      goto LABEL_63;
    case 2036687218:
      v12 = *(unsigned __int16 *)(a1 + 54);
      v5 = sub_14083D4F0(a1) + 40;
      LODWORD(v34) = v12;
      v33 = v5;
      if ( &v33 != a3 )
      {
        (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v13 = v33;
        v14 = v34;
        a3[1] = v34;
        *a3 = v13;
        v5 = sub_14083D4F0(v14) + 8;
        v34 = 0;
        v33 = v5;
      }
      goto LABEL_62;
    default:
      break;
  }
  return (unsigned int)v4;
}
