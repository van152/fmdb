void __fastcall sub_140809100(volatile signed __int32 **a1, volatile signed __int32 **a2)
{
  volatile signed __int32 *v3; // rdx
  volatile signed __int32 *v4; // rax
  volatile signed __int32 *v5; // rcx
  volatile signed __int32 *v6; // rdi
  volatile signed __int32 *v7; // rdi

  if ( a1 != a2 )
  {
    v3 = *a2;
    v4 = *a1;
    v5 = *a1 - 1;
    if ( v4 == nullptr )
      v5 = nullptr;
    v6 = v3 - 1;
    if ( v3 != nullptr )
    {
      if ( v4 != nullptr && _InterlockedDecrement(v5) == 0 )
        sub_1412EC9A0((__int64)v5);
      *a1 = nullptr;
      _InterlockedIncrement(v6);
      v7 = v6 + 1;
    }
    else
    {
      if ( v4 != nullptr && _InterlockedDecrement(v5) == 0 )
        sub_1412EC9A0((__int64)v5);
      v7 = nullptr;
    }
    *a1 = v7;
  }
}
