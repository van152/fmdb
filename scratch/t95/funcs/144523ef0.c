char __fastcall sub_144523EF0(_DWORD *a1, int a2, __int64 **a3)
{
  __int64 v4; // rdx
  volatile signed __int32 **v5; // rsi
  volatile signed __int32 *v6; // rax
  volatile signed __int32 *v7; // rcx
  volatile signed __int32 *v8; // rdi
  volatile signed __int32 *v9; // rdi
  __int64 v11; // rcx
  _QWORD v12[3]; // [rsp+20h] [rbp-18h] BYREF

  if ( a2 != 1382965613 )
    return sub_140FE2700(a1, a2, a3);
  (*(void (__fastcall **)(__int64 *, _QWORD *))(**a3 + 128))(*a3, v12);
  v5 = (volatile signed __int32 **)(a1 + 6);
  if ( v5 != v12 )
  {
    v4 = v12[0];
    v6 = *v5;
    v7 = *v5 - 1;
    if ( *v5 == nullptr )
      v7 = nullptr;
    v8 = (volatile signed __int32 *)(v12[0] - 4LL);
    if ( v12[0] != 0 )
    {
      if ( v6 != nullptr && _InterlockedDecrement(v7) == 0 )
        sub_1412EC9A0(v7, v4);
      *v5 = nullptr;
      _InterlockedIncrement(v8);
      v9 = v8 + 1;
    }
    else
    {
      if ( v6 != nullptr && _InterlockedDecrement(v7) == 0 )
        sub_1412EC9A0(v7, v4);
      v9 = nullptr;
    }
    *v5 = v9;
  }
  v11 = v12[0];
  if ( v12[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v12[0] - 4LL)) == 0 )
    sub_1412EC9A0(v11 - 4, v4);
  return 1;
}
