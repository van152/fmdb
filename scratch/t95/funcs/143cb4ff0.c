__int64 __fastcall sub_143CB4FF0(__int64 a1, _QWORD *a2, __int64 a3, unsigned int a4)
{
  _DWORD *v7; // rbx
  _DWORD *v8; // rbx
  __int64 v9; // rbx
  __int64 v10; // rbx
  __int64 v11; // rbx
  __int64 v12; // rbx
  __int64 v13; // rbx
  _QWORD *v15; // [rsp+28h] [rbp-30h] BYREF
  _DWORD v16[10]; // [rsp+30h] [rbp-28h] BYREF

  v7 = (_DWORD *)*a2;
  LOBYTE(v15) = 0;
  (*(void (__fastcall **)(_DWORD *, _QWORD **, __int64))(*(_QWORD *)v7 + 40LL))(v7, &v15, 1);
  if ( v7[4] != 0 )
    return 0;
  v8 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 240, 1);
  if ( v8[4] != 0 )
    return 0;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 241, 1);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return 0;
  v10 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 242, 1);
  if ( *(_DWORD *)(v10 + 16) != 0 )
    return 0;
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 228, 4);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return 0;
  v12 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 243, 1);
  if ( *(_DWORD *)(v12 + 16) != 0 )
    return 0;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 244, 1);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return 0;
  if ( (unsigned __int8)sub_14150F480(a1 + 72, a2) == 0 )
    return 0;
  if ( (_BYTE)a4 != 0
    && ((v15 = a2, (unsigned __int8)sub_140ED6BD0(&v15, a1 + 104) == 0)
     || (unsigned __int8)sub_140ED6BD0(&v15, a1 + 112) == 0
     || (unsigned __int8)sub_140ED6BD0(&v15, a1 + 120) == 0
     || (unsigned __int8)sub_140ED6BD0(&v15, a1 + 128) == 0
     || (unsigned __int8)sub_140ED6BD0(&v15, a1 + 136) == 0
     || (unsigned __int8)sub_140ED6BD0(&v15, a1 + 144) == 0
     || (sub_140838540(*a2, v16, a1 + 152), v16[0] != 0)
     || (sub_140838540(*a2, v16, a1 + 176), v16[0] != 0)) )
  {
    return 0;
  }
  else
  {
    return sub_140FE22B0(a1, a2, 0, a4);
  }
}
