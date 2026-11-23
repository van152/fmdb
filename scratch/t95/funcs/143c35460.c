__int64 __fastcall sub_143C35460(__int64 a1, char a2)
{
  __int64 **v2; // rax
  __int64 *v3; // r8
  __int64 *v4; // r9
  __int64 result; // rax
  __int64 v6; // r11
  __int64 *v7; // rax
  __int64 v8; // rdx

  v2 = *(__int64 ***)(qword_141B60118 + 128);
  v3 = *v2;
  v4 = v2[1];
  if ( *v2 == v4 )
  {
LABEL_8:
    if ( a2 != 0 )
    {
      v7 = *(__int64 **)(a1 + 24);
      if ( v7 == *(__int64 **)(a1 + 32) )
        LODWORD(v8) = 0;
      else
        v8 = *v7;
      return sub_140F8E3D0(
               (unsigned int)&qword_141B5FDA8,
               v8,
               0,
               0,
               0,
               0,
               0,
               0,
               0,
               0,
               -1,
               -1,
               -1,
               0,
               0,
               0,
               0,
               0,
               0,
               0,
               0);
    }
    else
    {
      return 0;
    }
  }
  else
  {
    while ( 1 )
    {
      result = *v3;
      if ( *(_BYTE *)(*v3 + 94) == 0 )
      {
        v6 = *(_QWORD *)(result + 24);
        if ( v6 != 0 && *(_DWORD *)(v6 + 12) == *(_DWORD *)(a1 + 12) )
          break;
      }
      if ( ++v3 == v4 )
        goto LABEL_8;
    }
  }
  return result;
}
