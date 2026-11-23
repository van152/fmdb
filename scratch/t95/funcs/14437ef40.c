__int64 __fastcall sub_14437EF40(__int64 a1, int a2, __int64 **a3)
{
  __int64 v5; // rbx
  __int64 *v6; // rcx
  __int64 *v7; // rax
  __int64 *v8; // rcx
  __int64 v9; // rcx
  int v10; // eax
  int v11; // ecx
  __int64 *v12; // rax
  __int64 *v13; // rcx
  int v14; // ebx
  __int64 v15; // rax
  __int64 *v16; // rax
  __int64 *v17; // rcx
  __int64 v18; // rcx
  __int64 v19; // rax
  __int64 *v20; // rax
  __int64 *v21; // rcx
  __int64 *v23; // [rsp+28h] [rbp-18h] BYREF
  __int64 *v24; // [rsp+30h] [rbp-10h]
  __int64 v25; // [rsp+38h] [rbp-8h]

  v25 = -2;
  LODWORD(v5) = 0;
  if ( a2 > 1952801132 )
  {
    if ( a2 == 1953132386 )
    {
      v14 = *(unsigned __int16 *)(a1 + 56);
      v15 = sub_14083D4F0(a1) + 56;
      LODWORD(v24) = v14;
      v23 = (__int64 *)v15;
      if ( &v23 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v16 = v23;
        v17 = v24;
        a3[1] = v24;
        *a3 = v16;
        v15 = sub_14083D4F0(v17) + 8;
        v24 = nullptr;
        v23 = (__int64 *)v15;
      }
      v5 = *(_QWORD *)v15;
      (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v15 + 16LL))(v15, &v23);
      LOBYTE(v5) = 1;
      if ( *(_WORD *)(a1 + 56) == 0 )
      {
        v19 = sub_14083D4F0(v18) + 56;
        LODWORD(v24) = 11;
        v23 = (__int64 *)v19;
        if ( &v23 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v20 = v23;
          v21 = v24;
          a3[1] = v24;
          *a3 = v20;
          v19 = sub_14083D4F0(v21) + 8;
          v24 = nullptr;
          v23 = (__int64 *)v19;
        }
        (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v19 + 16LL))(v19, &v23);
      }
    }
    else if ( a2 == 1952801133 )
    {
      v9 = *(_QWORD *)(a1 + 32);
      if ( v9 != 0 )
      {
        v10 = *(_DWORD *)(v9 + 12);
        v11 = *(_DWORD *)(v9 + 16);
        if ( v11 == 0 )
          v11 = v10;
      }
      else
      {
        v10 = -1;
        v11 = -1;
      }
      v23 = (__int64 *)__PAIR64__(v11, v10);
      sub_140FE72B0(&v23, 1416914273, a3);
      goto LABEL_26;
    }
  }
  else
  {
    if ( a2 == 1785686382 )
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
      LODWORD(v24) = ((*(_WORD *)(a1 + 40) & 0x1FF) << 8)
                   | (*(unsigned __int16 *)(a1 + 40) >> 9)
                   | (*(unsigned __int16 *)(a1 + 42) << 17);
      v6 = &qword_141B5C8A0;
      v23 = &qword_141B5C8A0;
      if ( &v23 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v12 = v23;
        v13 = v24;
        a3[1] = v24;
        *a3 = v12;
        v6 = (__int64 *)(sub_14083D4F0(v13) + 8);
        v24 = nullptr;
        v23 = v6;
      }
      goto LABEL_7;
    }
    if ( a2 == 1818584692 )
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
      LODWORD(v24) = ((*(_WORD *)(a1 + 44) & 0x1FF) << 8)
                   | (*(unsigned __int16 *)(a1 + 44) >> 9)
                   | (*(unsigned __int16 *)(a1 + 46) << 17);
      v6 = &qword_141B5C8A0;
      v23 = &qword_141B5C8A0;
      if ( &v23 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v7 = v23;
        v8 = v24;
        a3[1] = v24;
        *a3 = v7;
        v6 = (__int64 *)(sub_14083D4F0(v8) + 8);
        v24 = nullptr;
        v23 = v6;
      }
LABEL_7:
      (*(void (__fastcall **)(__int64 *, __int64 **))(*v6 + 16))(v6, &v23);
LABEL_26:
      LOBYTE(v5) = 1;
    }
  }
  return (unsigned int)v5;
}
