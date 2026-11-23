__int64 __fastcall sub_141198640(__int64 a1, int a2, __int64 **a3)
{
  __int64 v5; // rbx
  char v6; // bl
  __int64 v7; // rax
  __int64 *v8; // rax
  __int64 *v9; // rcx
  int v10; // edi
  __int64 *v11; // rax
  __int64 *v12; // rcx
  char v13; // bl
  __int64 *v14; // rax
  __int64 *v15; // rcx
  __int64 *v16; // rcx
  __int64 *v17; // rax
  __int64 *v18; // rcx
  __int64 *v19; // rax
  __int64 *v20; // rcx
  char v21; // bl
  __int64 *v22; // rax
  __int64 *v23; // rcx
  __int64 v24; // rcx
  int v25; // eax
  int v26; // ecx
  int v27; // edi
  __int64 *v28; // rax
  __int64 *v29; // rcx
  __int64 *v31; // [rsp+20h] [rbp-10h] BYREF
  __int64 *v32; // [rsp+28h] [rbp-8h]
  __int64 v33; // [rsp+30h] [rbp+0h]

  v33 = -2;
  LODWORD(v5) = 0;
  if ( a2 > 1886545267 )
  {
    if ( a2 <= 1936286820 )
    {
      if ( a2 == 1886545268 )
      {
        v21 = *(_BYTE *)(a1 + 52);
        v7 = sub_14083D4F0(a1) + 24;
        LOBYTE(v32) = v21;
        v31 = (__int64 *)v7;
        if ( &v31 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v22 = v31;
          v23 = v32;
          a3[1] = v32;
          *a3 = v22;
          v7 = sub_14083D4F0(v23) + 8;
          v32 = nullptr;
          v31 = (__int64 *)v7;
        }
        goto LABEL_39;
      }
      if ( a2 == 1936029285 )
      {
        v10 = *(char *)(a1 + 50);
        v7 = sub_14083D4F0(a1) + 40;
        LODWORD(v32) = v10;
        v31 = (__int64 *)v7;
        if ( &v31 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v11 = v31;
          v12 = v32;
          a3[1] = v32;
          *a3 = v11;
          v7 = sub_14083D4F0(v12) + 8;
          v32 = nullptr;
          v31 = (__int64 *)v7;
        }
        goto LABEL_39;
      }
      return (unsigned int)v5;
    }
    if ( a2 == 1936286821 )
    {
      v27 = *(unsigned __int8 *)(a1 + 51);
      if ( (unsigned __int8)(v27 - 1) <= 1u )
      {
        v7 = sub_14083D4F0(a1) + 40;
        LODWORD(v32) = v27;
        v31 = (__int64 *)v7;
        if ( &v31 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v28 = v31;
          v29 = v32;
          a3[1] = v32;
          *a3 = v28;
          v7 = sub_14083D4F0(v29) + 8;
          v32 = nullptr;
          v31 = (__int64 *)v7;
        }
        goto LABEL_39;
      }
      LOBYTE(v5) = 1;
      if ( a3 != (__int64 **)&qword_141B5A4A0 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        (*(void (__fastcall **)(__int64, __int64 *, __int64 **))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
          qword_141B5A4A0,
          &qword_141B5A4A0,
          a3);
      }
      return (unsigned int)v5;
    }
    if ( a2 != 1937007732 )
      return (unsigned int)v5;
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
    LODWORD(v32) = ((*(_WORD *)(a1 + 40) & 0x1FF) << 8)
                 | (*(unsigned __int16 *)(a1 + 40) >> 9)
                 | (*(unsigned __int16 *)(a1 + 42) << 17);
    v16 = &qword_141B5C8A0;
    v31 = &qword_141B5C8A0;
    if ( &v31 != a3 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
      v17 = v31;
      v18 = v32;
      a3[1] = v32;
      *a3 = v17;
      v16 = (__int64 *)(sub_14083D4F0(v18) + 8);
      v32 = nullptr;
      v31 = v16;
    }
    goto LABEL_24;
  }
  if ( a2 <= 1768843892 )
  {
    if ( a2 != 1701733492 )
    {
      if ( a2 == 1718973557 )
      {
        v6 = *(_BYTE *)(a1 + 48);
        v7 = sub_14083D4F0(a1) + 24;
        LOBYTE(v32) = v6;
        v31 = (__int64 *)v7;
        if ( &v31 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v8 = v31;
          v9 = v32;
          a3[1] = v32;
          *a3 = v8;
          v7 = sub_14083D4F0(v9) + 8;
          v32 = nullptr;
          v31 = (__int64 *)v7;
        }
LABEL_39:
        v5 = *(_QWORD *)v7;
        (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v7 + 16LL))(v7, &v31);
        goto LABEL_44;
      }
      return (unsigned int)v5;
    }
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
    LODWORD(v32) = ((*(_WORD *)(a1 + 44) & 0x1FF) << 8)
                 | (*(unsigned __int16 *)(a1 + 44) >> 9)
                 | (*(unsigned __int16 *)(a1 + 46) << 17);
    v16 = &qword_141B5C8A0;
    v31 = &qword_141B5C8A0;
    if ( &v31 != a3 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
      v19 = v31;
      v20 = v32;
      a3[1] = v32;
      *a3 = v19;
      v16 = (__int64 *)(sub_14083D4F0(v20) + 8);
      v32 = nullptr;
      v31 = v16;
    }
LABEL_24:
    (*(void (__fastcall **)(__int64 *, __int64 **))(*v16 + 16))(v16, &v31);
LABEL_44:
    LOBYTE(v5) = 1;
    return (unsigned int)v5;
  }
  if ( a2 == 1768843893 )
  {
    v24 = *(_QWORD *)(a1 + 32);
    if ( v24 != 0 )
    {
      v25 = *(_DWORD *)(v24 + 12);
      v26 = *(_DWORD *)(v24 + 16);
      if ( v26 == 0 )
        v26 = v25;
    }
    else
    {
      v25 = -1;
      v26 = -1;
    }
    v31 = (__int64 *)__PAIR64__(v26, v25);
    sub_140FE72B0(&v31, 1768843890, a3);
    goto LABEL_44;
  }
  if ( a2 == 1885696621 )
  {
    v13 = *(_BYTE *)(a1 + 49);
    v7 = sub_14083D4F0(a1) + 24;
    LOBYTE(v32) = v13;
    v31 = (__int64 *)v7;
    if ( &v31 != a3 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
      v14 = v31;
      v15 = v32;
      a3[1] = v32;
      *a3 = v14;
      v7 = sub_14083D4F0(v15) + 8;
      v32 = nullptr;
      v31 = (__int64 *)v7;
    }
    goto LABEL_39;
  }
  return (unsigned int)v5;
}
