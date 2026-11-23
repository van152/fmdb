// THUNK ALIAS -> sub_1436EEE40 (jmp:0x14080b890->0x1436eee40)
bool __fastcall sub_1436EEE40(_DWORD **a1, __int64 *a2)
{
  int v2; // r8d
  _DWORD *v3; // rax
  __int64 v4; // rdx
  __int64 v5; // rcx

  v2 = *((_DWORD *)a2 + 2);
  v3 = *a1;
  if ( v2 != -1 )
  {
    if ( v3 != nullptr )
    {
      if ( *v3 == v2 )
        goto LABEL_4;
    }
    else if ( v2 == 0 )
    {
      goto LABEL_4;
    }
    return false;
  }
LABEL_4:
  v4 = *a2;
  v5 = 0x1419435F1LL;
  if ( v3 != nullptr )
    v5 = (__int64)(v3 + 1);
  return (unsigned int)sub_141758D90(v5, v4) == 0;
}
