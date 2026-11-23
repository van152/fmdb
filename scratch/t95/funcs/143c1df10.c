__int64 __fastcall sub_143C1DF10(__int64 a1, char a2)
{
  int v2; // r8d
  __int64 v3; // r9
  __int64 *i; // rcx
  __int64 *v5; // rax
  unsigned int v6; // edx

  v2 = 1049072;
LABEL_2:
  v3 = a1;
  if ( (a2 & 1) != 0 )
  {
    for ( i = *(__int64 **)(a1 + 280); i != *(__int64 **)(v3 + 288); ++i )
    {
      v5 = (__int64 *)*i;
      if ( *(_QWORD *)(*i + 8) == v3 )
      {
        v6 = *((unsigned __int8 *)v5 + 48);
        if ( v6 <= 0x14 )
        {
          if ( _bittest(&v2, v6) )
          {
            a1 = *v5;
            a2 = 1;
            if ( *v5 != 0 )
              goto LABEL_2;
            return *(unsigned __int8 *)(*(_QWORD *)(v3 + 256) + 300LL);
          }
        }
      }
    }
  }
  return *(unsigned __int8 *)(*(_QWORD *)(v3 + 256) + 300LL);
}
