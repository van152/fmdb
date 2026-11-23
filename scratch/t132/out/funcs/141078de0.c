__int64 __fastcall sub_141078DE0(__int64 a1, __int64 **a2)
{
  unsigned int v2; // edi
  char v5; // al
  __int64 *v6; // rcx
  __int64 v7; // rsi
  __int64 *v8; // rbx
  __int64 v9; // rax
  __int64 v10; // rcx
  __int64 v11; // rdx
  __int64 v12; // rdx
  __int64 v13; // rax
  __int64 *v14; // rdx
  __int64 *v15; // r15
  _QWORD *v16; // r12
  __int64 v17; // rax
  __int64 v18; // rcx
  __int64 *v19; // rdx
  __int64 v20; // rcx
  __int64 v21; // rdx
  __int64 *v22; // rax
  int v23; // eax
  __int64 v24; // r14
  __int64 v25; // rdi
  __int64 v26; // rcx
  __int64 *v27; // rdx
  __int64 v28; // rax
  __int64 *v29; // rsi
  unsigned int v31; // eax

  v5 = (*(__int64 (__fastcall **)(__int64 *))(**a2 + 8))(a1: *a2);
  v6 = *a2;
  v7 = **a2;
  if ( v5 == 10 )
  {
    v2 = 0;
    v8 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v7 + 176))(a1: v6, a2, a3: 0);
    v9 = *v8;
    v10 = v8[1];
    if ( *v8 != v10 )
    {
      v11 = *v8;
      while ( *(_DWORD *)v11 != 1819504496 )
      {
        v11 += 16;
        if ( v11 == v10 )
          return 0;
      }
      if ( v11 != v10 && *(_QWORD *)(v11 + 8) != 0 )
      {
        v14 = nullptr;
        while ( *(_DWORD *)v9 != 1819504496 )
        {
          v9 += 16;
          if ( v9 == v10 )
            goto LABEL_24;
        }
        if ( v9 == v10 )
          v14 = nullptr;
        else
          v14 = *(__int64 **)(v9 + 8);
LABEL_24:
        v15 = &qword_141B5A4A0;
        if ( v14 == nullptr )
          v14 = &qword_141B5A4A0;
        v2 = 0;
        switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v14 + 64LL))(a1: *v14) )
        {
          case 1u:
            v16 = (_QWORD *)(a1 + 8);
            v17 = *v8;
            v18 = v8[1];
            v19 = nullptr;
            if ( *v8 != v18 )
            {
              while ( *(_DWORD *)v17 != 1869379180 )
              {
                v17 += 16;
                if ( v17 == v18 )
                  goto LABEL_42;
              }
              if ( v17 == v18 )
                v19 = nullptr;
              else
                v19 = *(__int64 **)(v17 + 8);
            }
LABEL_42:
            if ( v19 == nullptr )
              v19 = &qword_141B5A4A0;
            v23 = sub_1410790A0(a1: v16, a2: v19);
            if ( v23 < 0 )
              return 0;
            v24 = *v16 + 16LL * (unsigned int)v23;
            v25 = *v8;
            v26 = v8[1];
            v27 = nullptr;
            if ( *v8 == v26 )
            {
              v29 = &qword_141B5A4A0;
            }
            else
            {
              v28 = *v8;
              while ( *(_DWORD *)v28 != 1986096245 )
              {
                v28 += 16;
                if ( v28 == v26 )
                  goto LABEL_60;
              }
              if ( v28 == v26 )
                v27 = nullptr;
              else
                v27 = *(__int64 **)(v28 + 8);
LABEL_60:
              v29 = &qword_141B5A4A0;
              if ( v27 != nullptr )
                v29 = v27;
              v27 = nullptr;
              while ( *(_DWORD *)v25 != 1768169504 )
              {
                v25 += 16;
                if ( v25 == v26 )
                  goto LABEL_69;
              }
              if ( v25 == v26 )
                v27 = nullptr;
              else
                v27 = *(__int64 **)(v25 + 8);
            }
LABEL_69:
            if ( v27 != nullptr )
              v15 = v27;
            v31 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v15 + 80LL))(a1: *v15, a2: v15);
            return sub_1415D20B0(a1: v24, a2: v31, a3: v29);
          case 2u:
            v20 = *v8;
            v21 = v8[1];
            v22 = nullptr;
            if ( *v8 == v21 )
              goto LABEL_54;
            break;
          case 3u:
            LOBYTE(v2) = 1;
            return v2;
          case 5u:
            sub_140DD5C90(a1, a2: 0);
            LOBYTE(v2) = 1;
            return v2;
          default:
            return v2;
        }
        while ( *(_DWORD *)v20 != 1869379180 )
        {
          v20 += 16;
          if ( v20 == v21 )
            goto LABEL_54;
        }
        if ( v20 == v21 )
          v22 = nullptr;
        else
          v22 = *(__int64 **)(v20 + 8);
LABEL_54:
        if ( v22 != nullptr )
          v15 = v22;
        sub_1410790A0(a1: a1 + 8, a2: v15);
      }
      return 0;
    }
  }
  else
  {
    if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v7 + 8))(a1: v6, a2) != 11 )
      return 0;
    (*(void (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a2 + 184))(a1: *a2, a2, a3: 0);
    v13 = qword_141B60C30;
    if ( qword_141B60C30 == qword_141B60C38 )
      goto LABEL_11;
    while ( *(_DWORD *)v13 != 1986359923 )
    {
      v13 += 16;
      if ( v13 == qword_141B60C38 )
        goto LABEL_11;
    }
    if ( v13 == qword_141B60C38 || (LOBYTE(v2) = 1, *(_QWORD *)(v13 + 8) == 0) )
    {
LABEL_11:
      LOBYTE(v2) = 1;
      LOBYTE(v12) = 1;
      sub_140DD5C90(a1, a2: v12);
    }
  }
  return v2;
}
