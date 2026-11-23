char __fastcall sub_143F8B380(__int64 a1, __int64 a2, _QWORD *a3)
{
  volatile signed __int32 **v4; // rsi
  volatile signed __int32 *v5; // rax
  volatile signed __int32 *v6; // rcx
  volatile signed __int32 *v7; // rdi
  volatile signed __int32 *v8; // rdi
  __int64 v10; // rcx
  _QWORD v11[3]; // [rsp+20h] [rbp-18h] BYREF

  if ( (_DWORD)a2 == 1349742177 )
  {
    (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 128LL))(a1: *a3, a2: v11);
    v4 = (volatile signed __int32 **)(a1 + 40);
    if ( v4 == v11 )
      goto LABEL_19;
LABEL_6:
    v5 = *v4;
    v6 = *v4 - 1;
    if ( *v4 == nullptr )
      v6 = nullptr;
    v7 = (volatile signed __int32 *)(v11[0] - 4LL);
    if ( v11[0] != 0 )
    {
      if ( v5 != nullptr && _InterlockedDecrement(v6) == 0 )
        sub_1412EC9A0(a1: v6);
      *v4 = nullptr;
      _InterlockedIncrement(v7);
      v8 = v7 + 1;
    }
    else
    {
      if ( v5 != nullptr && _InterlockedDecrement(v6) == 0 )
        sub_1412EC9A0(a1: v6);
      v8 = nullptr;
    }
    *v4 = v8;
    goto LABEL_19;
  }
  if ( (_DWORD)a2 != 1348890209 )
    return sub_141084920(a1, a2, a3);
  (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 128LL))(a1: *a3, a2: v11);
  v4 = (volatile signed __int32 **)(a1 + 32);
  if ( v4 != v11 )
    goto LABEL_6;
LABEL_19:
  v10 = v11[0];
  if ( v11[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v11[0] - 4LL)) == 0 )
    sub_1412EC9A0(a1: v10 - 4);
  return 1;
}
