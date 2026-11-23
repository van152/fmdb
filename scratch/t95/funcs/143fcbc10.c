char __fastcall sub_143FCBC10(__int64 a1, int a2, __int64 **a3)
{
  int v5; // edi
  __int64 v6; // rax
  __int64 *v7; // rax
  __int64 *v8; // rcx
  __int64 *v9; // rcx
  __int64 *v10; // rax
  __int64 *v11; // rcx
  __int64 v13; // rdx
  __int64 v14; // rdx
  __int64 *v15; // [rsp+28h] [rbp-18h] BYREF
  __int64 *v16; // [rsp+30h] [rbp-10h]
  __int64 v17; // [rsp+38h] [rbp-8h]

  v17 = -2;
  if ( a2 == 1684108389 )
  {
    if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B5C8D0);
      if ( dword_141B5C8D0 == -1 )
      {
        qword_141B5C8A0 = 0x141759DF8LL;
        byte_141B5C8A8 = 32;
        LOBYTE(v13) = 32;
        sub_1412EA280(&qword_141B5C8B0, v13);
        LOBYTE(v14) = 32;
        sub_1412EB230(&qword_141B5C8C0, v14);
        qword_141B5C8A0 = 0x141876208LL;
        qword_141B5C8B0 = 0x1418762E8LL;
        qword_141B5C8C0 = 0x141876308LL;
        sub_141751048(sub_140DBCA10);
        sub_141750EA0(&dword_141B5C8D0);
      }
    }
    LODWORD(v16) = ((*(_WORD *)(a1 + 32) & 0x1FF) << 8)
                 | (*(unsigned __int16 *)(a1 + 32) >> 9)
                 | (*(unsigned __int16 *)(a1 + 34) << 17);
    v9 = &qword_141B5C8A0;
    v15 = &qword_141B5C8A0;
    if ( &v15 != a3 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
      v10 = v15;
      v11 = v16;
      a3[1] = v16;
      *a3 = v10;
      v9 = (__int64 *)(sub_14083D4F0(v11) + 8);
      v16 = nullptr;
      v15 = v9;
    }
    (*(void (__fastcall **)(__int64 *, __int64 **))(*v9 + 16))(v9, &v15);
    return 1;
  }
  if ( a2 == 1954115685 )
  {
    v5 = *(char *)(a1 + 36);
    v6 = sub_14083D4F0(a1) + 40;
    LODWORD(v16) = v5;
    v15 = (__int64 *)v6;
    if ( &v15 != a3 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
      v7 = v15;
      v8 = v16;
      a3[1] = v16;
      *a3 = v7;
      v6 = sub_14083D4F0(v8) + 8;
      v16 = nullptr;
      v15 = (__int64 *)v6;
    }
    (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v6 + 16LL))(v6, &v15);
    return 1;
  }
  return 0;
}
