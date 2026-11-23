// THUNK ALIAS -> sub_143EDB860 (jmp:0x14104dd70->0x143edb860)
__int64 __fastcall sub_143EDB860(__int64 a1, _QWORD *a2)
{
  _QWORD *v3; // rsi
  __int64 v4; // rdi
  unsigned __int64 v5; // rdi
  __int64 v6; // rcx
  __int64 v8; // rdx
  __int64 v9; // rdx
  __int64 *v10; // [rsp+20h] [rbp-10h] BYREF
  int v11; // [rsp+28h] [rbp-8h]
  __int64 v12; // [rsp+30h] [rbp+0h]

  v12 = -2;
  v3 = *(_QWORD **)(a1 + 192);
  v4 = *(_QWORD *)(a1 + 200) - (_QWORD)v3;
  if ( v4 != 0 )
  {
    v5 = v4 >> 4;
    v6 = 1;
    if ( v5 >= 2 )
      v6 = v5;
    while ( *v3 != *a2 )
    {
      v3 += 2;
      if ( --v6 == 0 )
        goto LABEL_6;
    }
    if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B5C8D0);
      if ( dword_141B5C8D0 == -1 )
      {
        qword_141B5C8A0 = 0x141759DF8LL;
        byte_141B5C8A8 = 32;
        LOBYTE(v8) = 32;
        sub_1412EA280(&qword_141B5C8B0, v8);
        LOBYTE(v9) = 32;
        sub_1412EB230(&qword_141B5C8C0, v9);
        qword_141B5C8A0 = 0x141876208LL;
        qword_141B5C8B0 = 0x1418762E8LL;
        qword_141B5C8C0 = 0x141876308LL;
        sub_141751048(sub_140DBCA10);
        sub_141750EA0(&dword_141B5C8D0);
      }
    }
    v11 = 249037056;
    v10 = &qword_141B5C8A0;
    sub_141070E80((__int64)v3, 1313305444, (__int64 *)&v10);
    (*(void (__fastcall **)(__int64 *, __int64 **))(*v10 + 16))(v10, &v10);
  }
  else
  {
LABEL_6:
    sub_1408C9770(a1 + 192, a2);
    return *(_QWORD *)(a1 + 200) - 16LL;
  }
  return (__int64)v3;
}
