__int64 __fastcall sub_14153DFE0(__int64 a1, int a2, __int64 **a3)
{
  __int64 v6; // rbx
  __int64 v7; // rax
  __int64 v8; // rcx
  __int64 **v9; // rcx
  __int64 v10; // rdx
  __int64 v11; // rcx
  int v12; // eax
  __int64 *v13; // rcx
  __int64 *v14; // rax
  __int64 *v15; // rcx
  int v16; // esi
  __int64 v17; // rax
  __int64 *v18; // rax
  __int64 *v19; // rcx
  int v20; // ecx
  int v21; // eax
  __int64 v22; // rbx
  __int64 v23; // rsi
  __int64 *v24; // rax
  __int64 *v25; // rcx
  __int64 *v26; // rax
  __int64 *v27; // rcx
  __int64 v28; // rsi
  __int64 v29; // r15
  __int64 v30; // rax
  __int64 v31; // rax
  int v32; // ecx
  int v33; // eax
  __int64 *v35; // [rsp+20h] [rbp-10h] BYREF
  __int64 *v36; // [rsp+28h] [rbp-8h]
  __int64 v37; // [rsp+30h] [rbp+0h]

  v37 = -2;
  LODWORD(v6) = 0;
  v7 = sub_140FE84D0();
  if ( a2 > 1886151032 )
  {
    if ( a2 == 2003136100 )
    {
      if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B5C8D0);
        if ( dword_141B5C8D0 == -1 )
        {
          sub_140DBC9B0(&qword_141B5C8A0);
          sub_141751048(sub_140DBCA10);
          sub_141750EA0(&dword_141B5C8D0);
        }
      }
      LODWORD(v36) = ((*(_WORD *)(a1 + 48) & 0x1FF) << 8)
                   | (*(unsigned __int16 *)(a1 + 48) >> 9)
                   | (*(unsigned __int16 *)(a1 + 50) << 17);
      v13 = &qword_141B5C8A0;
      v35 = &qword_141B5C8A0;
      if ( &v35 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v14 = v35;
        v15 = v36;
        a3[1] = v36;
        *a3 = v14;
        v13 = (__int64 *)(sub_14083D4F0(v15) + 8);
        v36 = nullptr;
        v35 = v13;
      }
      (*(void (__fastcall **)(__int64 *, __int64 **))(*v13 + 16))(v13, &v35);
      goto LABEL_45;
    }
    if ( a2 != 2002872165 )
    {
      if ( a2 == 1886151033 )
      {
        v9 = (__int64 **)(a1 + 24);
        v10 = 1348825715;
LABEL_44:
        sub_140FE72B0(v9, v10, a3);
        goto LABEL_45;
      }
      return (unsigned int)v6;
    }
    v16 = *(_DWORD *)(a1 + 52);
    v17 = sub_14083D4F0(v8) + 40;
    LODWORD(v36) = v16;
    v35 = (__int64 *)v17;
    if ( &v35 != a3 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
      v18 = v35;
      v19 = v36;
      a3[1] = v36;
      *a3 = v18;
      v17 = sub_14083D4F0(v19) + 8;
      v36 = nullptr;
      v35 = (__int64 *)v17;
    }
LABEL_32:
    v6 = *(_QWORD *)v17;
    (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v17 + 16LL))(v17, &v35);
LABEL_45:
    LOBYTE(v6) = 1;
    return (unsigned int)v6;
  }
  if ( a2 == 1668052322 )
  {
    if ( v7 != 0 )
    {
      v20 = *(_DWORD *)(v7 + 12);
      LODWORD(v35) = v20;
      v21 = *(_DWORD *)(v7 + 16);
      if ( v21 == 0 )
        v21 = v20;
    }
    else
    {
      LODWORD(v35) = -1;
      v20 = -1;
      v21 = -1;
    }
    v6 = qword_141B5FDB8;
    HIDWORD(v35) = v21;
    if ( v20 == *(_DWORD *)(a1 + 32) && v21 == *(_DWORD *)(a1 + 36)
      || (v28 = a1 + 32,
          v29 = (*(__int64 (__fastcall **)(__int64, __int64 **))(*(_QWORD *)qword_141B5FDB8 + 32LL))(
                  qword_141B5FDB8,
                  &v35),
          v30 = (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)v6 + 32LL))(v6, a1 + 32),
          v6 = qword_141B5FDB8,
          v29 == v30) )
    {
      v28 = a1 + 40;
    }
    v31 = sub_140F7A940(v6, v28);
    if ( v31 != 0 )
    {
      v32 = *(_DWORD *)(v31 + 12);
      v33 = *(_DWORD *)(v31 + 16);
      if ( v33 == 0 )
        v33 = v32;
    }
    else
    {
      v32 = -1;
      v33 = -1;
    }
    v35 = (__int64 *)__PAIR64__(v33, v32);
    v9 = &v35;
    v10 = 1130589301;
    goto LABEL_44;
  }
  if ( a2 == 1768124269 )
  {
    if ( v7 != 0 )
    {
      v11 = *(unsigned int *)(v7 + 12);
      LODWORD(v35) = *(_DWORD *)(v7 + 12);
      v12 = *(_DWORD *)(v7 + 16);
      if ( v12 == 0 )
        v12 = v11;
    }
    else
    {
      LODWORD(v35) = -1;
      v11 = 0xFFFFFFFFLL;
      v12 = -1;
    }
    v22 = qword_141B5FDB8;
    HIDWORD(v35) = v12;
    if ( (_DWORD)v11 == *(_DWORD *)(a1 + 40) && v12 == *(_DWORD *)(a1 + 44)
      || (v23 = (*(__int64 (__fastcall **)(__int64, __int64 **))(*(_QWORD *)qword_141B5FDB8 + 32LL))(
                  qword_141B5FDB8,
                  &v35)) == (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)v22 + 32LL))(v22, a1 + 40) )
    {
      v17 = sub_14083D4F0(v11) + 40;
      LODWORD(v36) = 1;
      v35 = (__int64 *)v17;
      if ( &v35 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v26 = v35;
        v27 = v36;
        a3[1] = v36;
        *a3 = v26;
        v17 = sub_14083D4F0(v27) + 8;
        v36 = nullptr;
        v35 = (__int64 *)v17;
      }
    }
    else
    {
      v17 = sub_14083D4F0(v11) + 40;
      LODWORD(v36) = 0;
      v35 = (__int64 *)v17;
      if ( &v35 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v24 = v35;
        v25 = v36;
        a3[1] = v36;
        *a3 = v24;
        v17 = sub_14083D4F0(v25) + 8;
        v36 = nullptr;
        v35 = (__int64 *)v17;
      }
    }
    goto LABEL_32;
  }
  return (unsigned int)v6;
}
