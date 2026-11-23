__int64 __fastcall sub_140809040(__int64 *a1, __int64 a2, int a3)
{
  int v4; // esi
  __int64 v5; // rbx
  volatile signed __int32 *v6; // rcx
  __int64 result; // rax
  volatile signed __int32 *v8; // rcx

  if ( a2 != 0 )
  {
    v4 = a3;
    if ( a3 == -1 )
    {
      v4 = sub_141758DB0(a2);
      if ( v4 > 0 )
      {
LABEL_4:
        v5 = sub_1412EC810(264, (unsigned int)v4);
        *(_DWORD *)v5 = 0;
        *(_DWORD *)(v5 + 4) = v4;
        sub_141758A00();
        *(_BYTE *)(v5 + (unsigned int)v4 + 8) = 0;
        if ( *a1 != 0 )
        {
          v6 = (volatile signed __int32 *)(*a1 - 4);
          if ( _InterlockedDecrement(v6) == 0 )
            sub_1412EC9A0((__int64)v6);
        }
        result = v5 + 4;
        *a1 = 0;
        _InterlockedIncrement((volatile signed __int32 *)v5);
        goto LABEL_13;
      }
    }
    else if ( a3 > 0 )
    {
      goto LABEL_4;
    }
  }
  v8 = (volatile signed __int32 *)(*a1 - 4);
  if ( *a1 != 0 && _InterlockedDecrement(v8) == 0 )
    sub_1412EC9A0((__int64)v8);
  result = 0;
LABEL_13:
  *a1 = result;
  return result;
}
